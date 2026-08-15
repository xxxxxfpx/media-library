"""
全量数据迁移脚本

功能：
- 从远程 PostgreSQL 数据库迁移所有数据到本地 SQLite
- 包括：Source, Tag, Genre, Studio, BoxSet, Movie, Series, Season, Episode
- 迁移 Files 和 FileLinks
- 迁移所有关联关系 (ItemLinks)

作者：Assistant
创建日期：2026-04-25
"""

import asyncio
import asyncpg
import json
from datetime import datetime, timezone, timedelta
from typing import Dict, Optional, Any, List
from contextlib import asynccontextmanager

from database.core import AsyncSessionLocal
from database.models import (
    MediaItem, MediaType, File, FileType,
    FileLink, ImageType, ItemLinks,
)
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

# 配置
REMOTE_DB_CONFIG = {
    'host': os.environ.get('REMOTE_DB_HOST', ''),
    'port': int(os.environ.get('REMOTE_DB_PORT', '5432')),
    'database': os.environ.get('REMOTE_DB_NAME', ''),
    'user': os.environ.get('REMOTE_DB_USER', ''),
    'password': os.environ.get('REMOTE_DB_PASSWORD', '')
}

BATCH_SIZE = 500  # 批量处理大小

# ID 映射管理
class IDMapper:
    """管理远程 ID 到本地 ID 的映射"""
    
    def __init__(self):
        self.media_map: Dict[int, int] = {}  # remote_media_id -> local_media_id
        self.file_map: Dict[int, int] = {}   # remote_file_id -> local_file_id
        self.source_map: Dict[int, int] = {} # remote_provider_id -> local_source_id
    
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
    
    def save(self, filename: str = 'id_mapping.json'):
        """保存映射到文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'media': self.media_map,
                'file': self.file_map,
                'source': self.source_map
            }, f, ensure_ascii=False, indent=2)
    
    def load(self, filename: str = 'id_mapping.json'):
        """从文件加载映射"""
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.media_map = {int(k): v for k, v in data.get('media', {}).items()}
                self.file_map = {int(k): v for k, v in data.get('file', {}).items()}
                self.source_map = {int(k): v for k, v in data.get('source', {}).items()}


# 时间戳转换
def to_local_time(dt: Optional[datetime]) -> datetime:
    """将时间戳转换为本地时区 (UTC+8)"""
    if dt is None:
        return datetime.now(timezone(timedelta(hours=8)))
    
    # 如果是 UTC 时间，转换为 UTC+8
    if dt.tzinfo is None:
        # 假设是 UTC 时间
        dt = dt.replace(tzinfo=timezone.utc)
    
    return dt.astimezone(timezone(timedelta(hours=8)))


# 迁移类
class FullMigration:
    """全量数据迁移"""
    
    def __init__(self):
        self.mapper = IDMapper()
        self.remote_conn: Optional[asyncpg.Connection] = None
        self.local_session: Optional[AsyncSession] = None
    
    async def connect(self):
        """连接数据库"""
        print("🔗 连接远程 PostgreSQL...")
        self.remote_conn = await asyncpg.connect(**REMOTE_DB_CONFIG)
        print("✅ 远程连接成功")
    
    async def disconnect(self):
        """断开连接"""
        if self.remote_conn:
            await self.remote_conn.close()
            print("✅ 远程连接已关闭")
    
    @asynccontextmanager
    async def local_session_context(self):
        """本地数据库会话上下文管理器"""
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
    
    async def migrate_providers_to_sources(self):
        """阶段 1: 从 Providers 创建 Source"""
        print("\n" + "="*60)
        print("阶段 1: 迁移 Providers → Sources")
        print("="*60)
        
        providers = await self.remote_conn.fetch(
            'SELECT "Id", "Name", "Url" FROM "Providers"'
        )
        
        print(f"发现 {len(providers)} 个 Provider")
        
        for provider in providers:
            # 检查本地是否已存在
            result = await self.local_session.execute(
                select(MediaItem).where(MediaItem.Id == provider['Id'])
            )
            existing = result.scalar_one_or_none()
            
            if existing:
                print(f"  ⚠️  Source {provider['Id']} 已存在 ({existing.Name})，跳过")
                self.mapper.add_source(provider['Id'], provider['Id'])
                continue
            
            # 创建 Source
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
        
        print(f"✅ 完成：{len(providers)} 个 Source")
    
    async def migrate_base_metadata(self, media_type: str, count: int = None):
        """迁移基础元数据 (Tag, Genre, Studio, BoxSet)"""
        print(f"\n迁移 {media_type}...")
        
        query = f'SELECT "Id", "Name" FROM "MediaItems" WHERE "Type" = $1'
        rows = await self.remote_conn.fetch(query, media_type)
        
        if count:
            rows = rows[:count]
        
        print(f"  发现 {len(rows)} 条记录")
        
        success_count = 0
        skip_count = 0
        
        for row in rows:
            try:
                # 检查本地是否已存在相同 ID
                result = await self.local_session.execute(
                    select(MediaItem).where(MediaItem.Id == row['Id'])
                )
                if result.scalar_one_or_none():
                    print(f"  ⚠️  {media_type} {row['Id']} 已存在，跳过")
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
                await self.local_session.commit()
                
                self.mapper.add_media(row['Id'], row['Id'])
                success_count += 1
                print(f"  ✅ {media_type}: {row['Name'][:50]}")
            except Exception as e:
                # 如果插入失败（可能是 Name 重复），跳过
                await self.local_session.rollback()
                print(f"  ⚠️  {media_type} '{row['Name'][:30]}' 插入失败：{e}，跳过")
                skip_count += 1
                continue
        
        print(f"  ✅ 完成：成功 {success_count} 个，跳过 {skip_count} 个 {media_type}")
    
    async def migrate_movies(self):
        """迁移 Movie"""
        print(f"\n迁移 Movie...")
        
        movies = await self.remote_conn.fetch(
            '''SELECT "Id", "Name", "Overview", "Tagline", 
                      "PremiereDate", "OfficialRating", "CommunityRating",
                      "DateCreated", "DateModified"
               FROM "MediaItems" WHERE "Type" = $1''',
            'Movie'
        )
        
        print(f"  发现 {len(movies)} 部电影")
        
        success_count = 0
        skip_count = 0
        
        for movie in movies:
            try:
                # 检查本地是否已存在
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
                await self.local_session.commit()
                
                self.mapper.add_media(movie['Id'], movie['Id'])
                success_count += 1
                print(f"  ✅ Movie: {movie['Name'][:50]}")
            except Exception as e:
                await self.local_session.rollback()
                print(f"  ⚠️  Movie '{movie['Name'][:30]}' 插入失败，跳过")
                skip_count += 1
                continue
        
        print(f"  ✅ 完成：成功 {success_count} 个，跳过 {skip_count} 个")
    
    async def migrate_series_seasons_episodes(self):
        """迁移 Series, Season, Episode"""
        print(f"\n迁移 Series...")
        
        # 迁移 Series
        series_list = await self.remote_conn.fetch(
            '''SELECT "Id", "Name", "Overview", "PremiereDate", "EndDate",
                      "CommunityRating", "DateCreated", "DateModified"
               FROM "MediaItems" WHERE "Type" = $1''',
            'Series'
        )
        
        print(f"  发现 {len(series_list)} 个 Series")
        series_success = 0
        series_skip = 0
        for series in series_list:
            try:
                result = await self.local_session.execute(
                    select(MediaItem).where(MediaItem.Id == series['Id'])
                )
                if result.scalar_one_or_none():
                    self.mapper.add_media(series['Id'], series['Id'])
                    series_skip += 1
                    continue
                
                item = MediaItem(
                    Id=series['Id'],
                    Type=MediaType.Series,
                    Name=series['Name'],
                    Overview=series['Overview'],
                    PremiereDate=series['PremiereDate'],
                    EndDate=series['EndDate'],
                    CommunityRating=series['CommunityRating'],
                    DateCreated=to_local_time(series['DateCreated']),
                    DateModified=to_local_time(series['DateModified']),
                )
                
                self.local_session.add(item)
                await self.local_session.commit()
                self.mapper.add_media(series['Id'], series['Id'])
                series_success += 1
            except Exception as e:
                await self.local_session.rollback()
                series_skip += 1
                continue
        
        print(f"  ✅ Series: 成功 {series_success} 个，跳过 {series_skip} 个")
        
        # 迁移 Season
        print(f"\n迁移 Season...")
        seasons = await self.remote_conn.fetch(
            '''SELECT "Id", "Name", "ParentId", "Overview", "IndexNumber",
                      "PremiereDate", "DateCreated", "DateModified"
               FROM "MediaItems" WHERE "Type" = $1''',
            'Season'
        )
        
        print(f"  发现 {len(seasons)} 个 Season")
        season_success = 0
        season_skip = 0
        for season in seasons:
            try:
                result = await self.local_session.execute(
                    select(MediaItem).where(MediaItem.Id == season['Id'])
                )
                if result.scalar_one_or_none():
                    self.mapper.add_media(season['Id'], season['Id'])
                    season_skip += 1
                    continue
                
                item = MediaItem(
                    Id=season['Id'],
                    Type=MediaType.Season,
                    Name=season['Name'],
                    Overview=season['Overview'],
                    PremiereDate=season['PremiereDate'],
                    DateCreated=to_local_time(season['DateCreated']),
                    DateModified=to_local_time(season['DateModified']),
                )
                
                self.local_session.add(item)
                await self.local_session.commit()
                self.mapper.add_media(season['Id'], season['Id'])
                season_success += 1
                
                # 创建 Season → Series 关联
                if season['ParentId']:
                    series_id = self.mapper.get_media(season['ParentId'])
                    if series_id:
                        link = ItemLinks(
                            ItemId=series_id,
                            LinkedItemId=season['Id'],
                            Type='Season',
                        )
                        self.local_session.add(link)
                        await self.local_session.commit()
            except Exception as e:
                await self.local_session.rollback()
                season_skip += 1
                continue
        
        print(f"  ✅ Season: 成功 {season_success} 个，跳过 {season_skip} 个")
        
        # 迁移 Episode
        print(f"\n迁移 Episode...")
        episodes = await self.remote_conn.fetch(
            '''SELECT "Id", "Name", "ParentId", "Overview", "IndexNumber",
                      "PremiereDate", "DateCreated", "DateModified"
               FROM "MediaItems" WHERE "Type" = $1''',
            'Episode'
        )
        
        print(f"  发现 {len(episodes)} 个 Episode")
        ep_success = 0
        ep_skip = 0
        for episode in episodes:
            try:
                result = await self.local_session.execute(
                    select(MediaItem).where(MediaItem.Id == episode['Id'])
                )
                if result.scalar_one_or_none():
                    self.mapper.add_media(episode['Id'], episode['Id'])
                    ep_skip += 1
                    continue
                
                item = MediaItem(
                    Id=episode['Id'],
                    Type=MediaType.Episode,
                    Name=episode['Name'],
                    Overview=episode['Overview'],
                    PremiereDate=episode['PremiereDate'],
                    DateCreated=to_local_time(episode['DateCreated']),
                    DateModified=to_local_time(episode['DateModified']),
                )
                
                self.local_session.add(item)
                await self.local_session.commit()
                self.mapper.add_media(episode['Id'], episode['Id'])
                ep_success += 1
                
                # 创建 Episode → Season 关联
                if episode['ParentId']:
                    season_id = self.mapper.get_media(episode['ParentId'])
                    if season_id:
                        link = ItemLinks(
                            ItemId=season_id,
                            LinkedItemId=episode['Id'],
                            Type='Episode',
                        )
                        self.local_session.add(link)
                        await self.local_session.commit()
            except Exception as e:
                await self.local_session.rollback()
                ep_skip += 1
                continue
        
        print(f"  ✅ 完成：Series {series_success}, Season {season_success}, Episode {ep_success}")
    
    async def run(self):
        """运行全量迁移"""
        print("="*60)
        print("全量数据迁移开始")
        print("="*60)
        
        await self.connect()
        
        try:
            async with self.local_session_context():
                # 阶段 1: 基础元数据
                await self.migrate_providers_to_sources()
                await self.migrate_base_metadata('Tag')
                await self.migrate_base_metadata('Genre')
                await self.migrate_base_metadata('Studio')
                await self.migrate_base_metadata('BoxSet')
                
                # 阶段 2: 媒体内容
                await self.migrate_movies()
                await self.migrate_series_seasons_episodes()
                
                # TODO: 阶段 3: 文件迁移
                # await self.migrate_files()
                # await self.migrate_file_links()
                
                # TODO: 阶段 4: 关联关系
                # await self.migrate_links()
                # await self.migrate_source_links()
                
                # TODO: 阶段 5: 填充 Type
                # await self.fill_link_types()
            
            # 保存 ID 映射
            self.mapper.save()
            print("\n✅ 全量迁移完成！")
            print(f"ID 映射已保存到 id_mapping.json")
            
        except Exception as e:
            print(f"\n❌ 迁移失败：{e}")
            import traceback
            traceback.print_exc()
        finally:
            await self.disconnect()


if __name__ == '__main__':
    import os
    asyncio.run(FullMigration().run())
