"""
迁移 Hanime Provider 的数据

只迁移 ProviderId=1 (Hanime) 关联的所有数据
"""

import os
import asyncio
import asyncpg
import json
from datetime import datetime, timezone, timedelta
from typing import Dict, Optional
from contextlib import asynccontextmanager

from database.core import AsyncSessionLocal
from database.models import (
    MediaItem, MediaType, File, FileType,
    FileLink, ImageType, ItemLinks,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# 配置
REMOTE_DB_CONFIG = {
    'host': os.environ.get('REMOTE_DB_HOST', ''),
    'port': int(os.environ.get('REMOTE_DB_PORT', '5432')),
    'database': os.environ.get('REMOTE_DB_NAME', ''),
    'user': os.environ.get('REMOTE_DB_USER', ''),
    'password': os.environ.get('REMOTE_DB_PASSWORD', '')
}

HANIME_PROVIDER_ID = 1  # Hanime 的 Provider ID

# ID 映射管理
class IDMapper:
    def __init__(self):
        self.media_map: Dict[int, int] = {}
        self.file_map: Dict[int, int] = {}
        self.source_map: Dict[int, int] = {}
    
    def add_media(self, remote_id: int, local_id: int):
        self.media_map[remote_id] = local_id
    
    def add_file(self, remote_id: int, local_id: int):
        self.file_map[remote_id] = local_id
    
    def add_source(self, remote_id: int, local_id: int):
        self.source_map[remote_id] = local_id
    
    def get_media(self, remote_id: int) -> Optional[int]:
        return self.media_map.get(remote_id)
    
    def get_file(self, remote_id: int) -> Optional[int]:
        return self.file_map.get(remote_id)
    
    def get_source(self, remote_id: int) -> Optional[int]:
        return self.source_map.get(remote_id)
    
    def save(self, filename: str = 'id_mapping_hanime.json'):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'media': self.media_map,
                'file': self.file_map,
                'source': self.source_map
            }, f, ensure_ascii=False, indent=2)


def to_local_time(dt):
    if dt is None:
        return datetime.now(timezone(timedelta(hours=8)))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone(timedelta(hours=8)))


class HanimeMigration:
    def __init__(self):
        self.mapper = IDMapper()
        self.remote_conn = None
        self.local_session = None
    
    async def connect(self):
        print("🔗 连接远程 PostgreSQL...")
        self.remote_conn = await asyncpg.connect(**REMOTE_DB_CONFIG)
        print("✅ 远程连接成功")
    
    async def disconnect(self):
        if self.remote_conn:
            await self.remote_conn.close()
            print("✅ 远程连接已关闭")
    
    @asynccontextmanager
    async def local_session_context(self):
        async with AsyncSessionLocal() as session:
            self.local_session = session
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                self.local_session = None
    
    async def migrate_hanime_source(self):
        """迁移 Hanime Provider 为 Source"""
        print("\n" + "="*60)
        print("阶段 1: 迁移 Hanime Provider → Source")
        print("="*60)
        
        provider = await self.remote_conn.fetchrow(
            'SELECT "Id", "Name", "Url" FROM "Providers" WHERE "Id" = $1',
            HANIME_PROVIDER_ID
        )
        
        if not provider:
            print("❌ 未找到 Hanime Provider")
            return
        
        source = MediaItem(
            Id=provider['Id'],
            Type=MediaType.Source,
            Name=provider['Name'],
            Overview=provider.get('Url'),
            DateCreated=datetime.now(timezone(timedelta(hours=8))),
            DateModified=datetime.now(timezone(timedelta(hours=8))),
        )
        
        self.local_session.add(source)
        await self.local_session.commit()
        
        self.mapper.add_source(provider['Id'], provider['Id'])
        print(f"  ✅ Source: {provider['Name']} (ID: {provider['Id']})")
    
    async def migrate_hanime_metadata(self, media_type: str):
        """迁移 Hanime 关联的基础元数据"""
        print(f"\n迁移 Hanime 的 {media_type}...")
        
        # 通过 ItemProviders 获取 Hanime 关联的 MediaItems
        rows = await self.remote_conn.fetch('''
            SELECT mi."Id", mi."Name"
            FROM "ItemProviders" ip
            JOIN "MediaItems" mi ON ip."ItemId" = mi."Id"
            WHERE ip."ProviderId" = $1 AND mi."Type" = $2
        ''', HANIME_PROVIDER_ID, media_type)
        
        print(f"  发现 {len(rows)} 条记录")
        
        success_count = 0
        skip_count = 0
        
        for row in rows:
            try:
                # 检查本地是否已存在
                result = await self.local_session.execute(
                    select(MediaItem).where(MediaItem.Id == row['Id'])
                )
                existing = result.scalar_one_or_none()
                if existing:
                    self.mapper.add_media(row['Id'], row['Id'])
                    skip_count += 1
                    continue
                
                item = MediaItem(
                    Id=row['Id'],
                    Type=MediaType(media_type),
                    Name=row['Name'],
                    DateCreated=datetime.now(timezone(timedelta(hours=8))),
                    DateModified=datetime.now(timezone(timedelta(hours=8))),
                )
                
                self.local_session.add(item)
                await self.local_session.flush()
                
                self.mapper.add_media(row['Id'], row['Id'])
                success_count += 1
                if success_count % 100 == 0:
                    await self.local_session.commit()
                    print(f"  ✅ {media_type}: {row['Name'][:50]} (已提交 {success_count} 个)")
            except Exception as e:
                await self.local_session.rollback()
                print(f"  ⚠️  {media_type} '{row['Name'][:30]}' 插入失败：{type(e).__name__}, 跳过")
                skip_count += 1
                continue
        
        # 最后提交一次
        await self.local_session.commit()
        print(f"  ✅ 完成：成功 {success_count} 个，跳过 {skip_count} 个")
    
    async def migrate_hanime_movies(self):
        """迁移 Hanime 关联的 Movie"""
        print(f"\n迁移 Hanime 的 Movie...")
        
        movies = await self.remote_conn.fetch('''
            SELECT mi."Id", mi."Name", mi."Overview", mi."Tagline",
                   mi."PremiereDate", mi."OfficialRating", mi."CommunityRating",
                   mi."DateCreated", mi."DateModified"
            FROM "ItemProviders" ip
            JOIN "MediaItems" mi ON ip."ItemId" = mi."Id"
            WHERE ip."ProviderId" = $1 AND mi."Type" = $2
        ''', HANIME_PROVIDER_ID, 'Movie')
        
        print(f"  发现 {len(movies)} 部电影")
        
        success_count = 0
        skip_count = 0
        
        for movie in movies:
            try:
                result = await self.local_session.execute(
                    select(MediaItem).where(MediaItem.Id == movie['Id'])
                )
                if result.scalar_one_or_none():
                    self.mapper.add_media(movie['Id'], movie['Id'])
                    skip_count += 1
                    continue
                
                item = MediaItem(
                    Id=movie['Id'],
                    Type=MediaType.Movie,
                    Name=movie['Name'],
                    Overview=movie['Overview'],
                    Tagline=movie['Tagline'],
                    PremiereDate=movie['PremiereDate'],
                    OfficialRating=movie['OfficialRating'],
                    CommunityRating=movie['CommunityRating'],
                    DateCreated=to_local_time(movie['DateCreated']),
                    DateModified=to_local_time(movie['DateModified']),
                )
                
                self.local_session.add(item)
                await self.local_session.flush()
                
                self.mapper.add_media(movie['Id'], movie['Id'])
                success_count += 1
                if success_count % 100 == 0:
                    await self.local_session.commit()
                    print(f"  ✅ Movie: {movie['Name'][:50]} (已提交 {success_count} 个)")
            except Exception as e:
                await self.local_session.rollback()
                print(f"  ⚠️  Movie '{movie['Name'][:30]}' 插入失败：{type(e).__name__}, 跳过")
                skip_count += 1
                continue
        
        await self.local_session.commit()
        print(f"  ✅ 完成：成功 {success_count} 个，跳过 {skip_count} 个")
    
    async def migrate_hanime_series_seasons_episodes(self):
        """迁移 Hanime 关联的 Series, Season, Episode"""
        print(f"\n迁移 Hanime 的 Series...")
        
        for media_type in ['Series', 'Season', 'Episode']:
            print(f"\n迁移 Hanime 的 {media_type}...")
            
            items = await self.remote_conn.fetch('''
                SELECT mi."Id", mi."Name", mi."Overview", mi."ParentId",
                       mi."PremiereDate", mi."EndDate", mi."CommunityRating",
                       mi."DateCreated", mi."DateModified"
                FROM "ItemProviders" ip
                JOIN "MediaItems" mi ON ip."ItemId" = mi."Id"
                WHERE ip."ProviderId" = $1 AND mi."Type" = $2
            ''', HANIME_PROVIDER_ID, media_type)
            
            print(f"  发现 {len(items)} 个 {media_type}")
            
            success_count = 0
            skip_count = 0
            
            for item_data in items:
                try:
                    result = await self.local_session.execute(
                        select(MediaItem).where(MediaItem.Id == item_data['Id'])
                    )
                    if result.scalar_one_or_none():
                        self.mapper.add_media(item_data['Id'], item_data['Id'])
                        skip_count += 1
                        continue
                    
                    item = MediaItem(
                        Id=item_data['Id'],
                        Type=MediaType(media_type),
                        Name=item_data['Name'],
                        Overview=item_data['Overview'],
                        PremiereDate=item_data['PremiereDate'],
                        EndDate=item_data.get('EndDate'),
                        CommunityRating=item_data.get('CommunityRating'),
                        DateCreated=to_local_time(item_data['DateCreated']),
                        DateModified=to_local_time(item_data['DateModified']),
                    )
                    
                    self.local_session.add(item)
                    await self.local_session.flush()
                    
                    self.mapper.add_media(item_data['Id'], item_data['Id'])
                    success_count += 1
                    
                    # 创建层级关联
                    if item_data['ParentId']:
                        parent_id = self.mapper.get_media(item_data['ParentId'])
                        if parent_id:
                            link_type = 'Season' if media_type == 'Season' else 'Episode'
                            link = ItemLinks(
                                ItemId=parent_id,
                                LinkedItemId=item_data['Id'],
                                Type=link_type,
                            )
                            self.local_session.add(link)
                            await self.local_session.flush()
                    
                    if success_count % 50 == 0:
                        await self.local_session.commit()
                        print(f"  ✅ {media_type}: {item_data['Name'][:50]} (已提交 {success_count} 个)")
                except Exception as e:
                    await self.local_session.rollback()
                    print(f"  ⚠️  {media_type} '{item_data['Name'][:30]}' 插入失败：{type(e).__name__}, 跳过")
                    skip_count += 1
                    continue
            
            await self.local_session.commit()
            print(f"  ✅ {media_type}: 成功 {success_count} 个，跳过 {skip_count} 个")
    
    async def migrate_hanime_links(self, link_type: str):
        """迁移 Hanime 关联的 Genre/Studio/Tag/BoxSet 关联"""
        print(f"\n迁移 Hanime 的 {link_type} 关联...")
        
        # 获取所有 Hanime 关联的 MediaItem IDs
        item_ids = await self.remote_conn.fetch('''
            SELECT ip."ItemId"
            FROM "ItemProviders" ip
            JOIN "MediaItems" mi ON ip."ItemId" = mi."Id"
            WHERE ip."ProviderId" = $1 AND mi."Type" IN ('Movie', 'Episode')
        ''', HANIME_PROVIDER_ID)
        
        item_id_list = [r['ItemId'] for r in item_ids]
        
        if not item_id_list:
            print("  没有找到关联项")
            return
        
        # 分批查询，避免 SQL 过长
        batch_size = 1000
        total_links = 0
        
        for i in range(0, len(item_id_list), batch_size):
            batch_ids = item_id_list[i:i+batch_size]
            
            # 查询这些 Item 关联的 Genre/Studio/Tag/BoxSet
            links = await self.remote_conn.fetch(f'''
                SELECT il."ItemId", il."LinkedItemId"
                FROM "ItemLinks" il
                JOIN "MediaItems" mi ON il."LinkedItemId" = mi."Id"
                WHERE il."ItemId" = ANY($1::int[]) AND mi."Type" = $2
            ''', batch_ids, link_type)
            
            for link_data in links:
                try:
                    local_item_id = self.mapper.get_media(link_data['ItemId'])
                    local_linked_id = self.mapper.get_media(link_data['LinkedItemId'])
                    
                    if local_item_id and local_linked_id:
                        link = ItemLinks(
                            ItemId=local_item_id,
                            LinkedItemId=local_linked_id,
                            Type=link_type,
                        )
                        self.local_session.add(link)
                        total_links += 1
                        if total_links % 500 == 0:
                            await self.local_session.commit()
                except Exception as e:
                    await self.local_session.rollback()
                    continue
        
        await self.local_session.commit()
        print(f"  ✅ 创建 {total_links} 个 {link_type} 关联")
    
    async def migrate_hanime_source_links(self):
        """创建所有 Hanime 元素 → Source 的关联"""
        print(f"\n创建 Hanime 元素 → Source 关联...")
        
        # 获取所有 Hanime 关联的 MediaItem IDs
        item_ids = await self.remote_conn.fetch('''
            SELECT ip."ItemId"
            FROM "ItemProviders" ip
            JOIN "MediaItems" mi ON ip."ItemId" = mi."Id"
            WHERE ip."ProviderId" = $1
        ''', HANIME_PROVIDER_ID)
        
        print(f"  需要创建 {len(item_ids)} 个 Source 关联")
        
        success_count = 0
        for item_data in item_ids:
            try:
                local_item_id = self.mapper.get_media(item_data['ItemId'])
                local_source_id = self.mapper.get_source(HANIME_PROVIDER_ID)
                
                if local_item_id and local_source_id:
                    link = ItemLinks(
                        ItemId=local_item_id,
                        LinkedItemId=local_source_id,
                        Type='Source',
                    )
                    self.local_session.add(link)
                    success_count += 1
                    if success_count % 500 == 0:
                        await self.local_session.commit()
            except Exception as e:
                await self.local_session.rollback()
                continue
        
        await self.local_session.commit()
        print(f"  ✅ 创建 {success_count} 个 Source 关联")
    
    async def run(self):
        """运行迁移"""
        print("="*60)
        print("开始迁移 Hanime Provider 数据")
        print("="*60)
        
        await self.connect()
        
        try:
            async with self.local_session_context():
                # 阶段 1: 创建 Source
                await self.migrate_hanime_source()
                
                # 阶段 2: 基础元数据
                await self.migrate_hanime_metadata('Tag')
                await self.migrate_hanime_metadata('Genre')
                await self.migrate_hanime_metadata('Studio')
                await self.migrate_hanime_metadata('BoxSet')
                
                # 阶段 3: 媒体内容
                await self.migrate_hanime_movies()
                await self.migrate_hanime_series_seasons_episodes()
                
                # 阶段 4: 关联关系
                await self.migrate_hanime_links('Tag')
                await self.migrate_hanime_links('Genre')
                await self.migrate_hanime_links('Studio')
                await self.migrate_hanime_links('BoxSet')
                
                # 阶段 5: Source 关联
                await self.migrate_hanime_source_links()
            
            # 保存 ID 映射
            self.mapper.save()
            print("\n✅ Hanime 数据迁移完成！")
            print(f"ID 映射已保存到 id_mapping_hanime.json")
            
        except Exception as e:
            print(f"\n❌ 迁移失败：{e}")
            import traceback
            traceback.print_exc()
        finally:
            await self.disconnect()


if __name__ == '__main__':
    asyncio.run(HanimeMigration().run())
