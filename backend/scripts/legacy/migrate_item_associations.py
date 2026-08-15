"""
迁移单个视频的伴生属性
用法: python migrate_item_associations.py <item_id>
示例: python migrate_item_associations.py 100
"""
import os
import asyncio
import asyncpg
import json
import sys
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from database.core import AsyncSessionLocal
from database.models import (
    MediaItem, MediaType, ItemLinks, LinkType,
    FileLink, ImageType, PeopleType
)
from sqlalchemy import select

REMOTE_DB_CONFIG = {
    'host': os.environ.get('REMOTE_DB_HOST', ''),
    'port': int(os.environ.get('REMOTE_DB_PORT', '5432')),
    'database': os.environ.get('REMOTE_DB_NAME', ''),
    'user': os.environ.get('REMOTE_DB_USER', ''),
    'password': os.environ.get('REMOTE_DB_PASSWORD', '')
}


class AssociationMigrator:
    def __init__(self, remote_conn, local_session):
        self.remote_conn = remote_conn
        self.local_session = local_session
        self.stats = {}

    async def migrate_item_links(self, item_id):
        """迁移 ItemLinks - 通用关联关系"""
        print(f"\n🔗 迁移 ItemLinks (通用关联)...")
        
        rows = await self.remote_conn.fetch(
            '''SELECT "LinkedItemId", "Order"
               FROM "ItemLinks" 
               WHERE "ItemId" = $1
               ORDER BY "Order"''',
            item_id
        )
        
        for row in rows:
            link = ItemLinks(
                ItemId=item_id,
                LinkedItemId=row['LinkedItemId'],
                Type=LinkType.Season,  # 默认类型
            )
            self.local_session.add(link)
        
        await self.local_session.commit()
        self.stats['item_links'] = len(rows)
        print(f"  ✅ {len(rows)} 条关联")

    async def migrate_item_people(self, item_id):
        """迁移 ItemPeople - 人物关联"""
        print(f"\n👥 迁移 ItemPeople (人物关联)...")
        
        rows = await self.remote_conn.fetch(
            '''SELECT "PersonId", "Role", "Type", "Order"
               FROM "ItemPeople" 
               WHERE "ItemId" = $1
               ORDER BY "Order"''',
            item_id
        )
        
        people_type_map = {
            'Actor': PeopleType.Actor,
            'Director': PeopleType.Director,
            'Writer': PeopleType.Writer,
            'Producer': PeopleType.Producer,
        }
        
        for row in rows:
            people_type = people_type_map.get(row['Type'], PeopleType.Actor)
            
            link = ItemLinks(
                ItemId=item_id,
                LinkedItemId=row['PersonId'],
                Type=LinkType.Person,
                PeopleType=people_type,
                PeopleRole=row['Role'],
            )
            self.local_session.add(link)
        
        await self.local_session.commit()
        self.stats['item_people'] = len(rows)
        print(f"  ✅ {len(rows)} 个人物关联")

    async def migrate_item_sources(self, item_id):
        """迁移 ItemSources - 来源关联"""
        print(f"\n📡 迁移 ItemSources (来源关联)...")
        
        rows = await self.remote_conn.fetch(
            '''SELECT "FileId", "Type"
               FROM "ItemSources" 
               WHERE "ItemId" = $1''',
            item_id
        )
        
        for row in rows:
            link = ItemLinks(
                ItemId=item_id,
                LinkedItemId=row['FileId'],  # FileId 作为 LinkedItemId
                Type=LinkType.Source,
            )
            self.local_session.add(link)
        
        await self.local_session.commit()
        self.stats['item_sources'] = len(rows)
        print(f"  ✅ {len(rows)} 个来源关联")

    async def migrate_item_providers(self, item_id):
        """迁移 ItemProviders - 提供者关联"""
        print(f"\n🏢 迁移 ItemProviders (提供者关联)...")
        
        rows = await self.remote_conn.fetch(
            '''SELECT "Type", "SourceId", "ProviderId", "Url"
               FROM "ItemProviders" 
               WHERE "ItemId" = $1''',
            item_id
        )
        
        for row in rows:
            # ItemProviders 转换为 ItemLinks，ProviderId 映射为 LinkedItemId
            link = ItemLinks(
                ItemId=item_id,
                LinkedItemId=row['ProviderId'],
                Type=LinkType.Source,  # 提供者作为 Source 类型关联
            )
            self.local_session.add(link)
        
        await self.local_session.commit()
        self.stats['item_providers'] = len(rows)
        print(f"  ✅ {len(rows)} 个提供者关联")

    async def migrate_file_images(self, item_id):
        """迁移 FileImages - 文件图片"""
        print(f"\n🖼️  迁移 FileImages (文件图片)...")
        
        rows = await self.remote_conn.fetch(
            '''SELECT "FileId", "Type", "ImageIndex"
               FROM "FileImages" 
               WHERE "ItemId" = $1
               ORDER BY "ImageIndex"''',
            item_id
        )
        
        image_type_map = {
            'Primary': ImageType.Primary,
            'Backdrop': ImageType.Backdrop,
            'Logo': ImageType.Logo,
            'Thumb': ImageType.Thumb,
        }
        
        for row in rows:
            image_type = image_type_map.get(row['Type'], ImageType.Primary)
            
            link = FileLink(
                ItemId=item_id,
                FileId=row['FileId'],
                ImageType=image_type,
                ImageIndex=row['ImageIndex'] or 0,
            )
            self.local_session.add(link)
        
        await self.local_session.commit()
        self.stats['file_images'] = len(rows)
        print(f"  ✅ {len(rows)} 个文件图片")

    async def migrate_all(self, item_id):
        """迁移所有伴生属性"""
        print(f"\n{'='*60}")
        print(f"开始迁移视频 ID={item_id} 的伴生属性")
        print(f"{'='*60}")
        
        # 检查媒体是否存在
        result = await self.local_session.execute(
            select(MediaItem).where(MediaItem.Id == item_id)
        )
        media = result.scalar_one_or_none()
        
        if not media:
            print(f"❌ 本地数据库中不存在 ID={item_id} 的媒体项")
            return False
        
        print(f"📺 媒体名称: {media.Name}")
        print(f"📂 媒体类型: {media.Type.value if media.Type else 'Unknown'}")
        
        # 迁移各类伴生属性
        await self.migrate_item_links(item_id)
        await self.migrate_item_people(item_id)
        await self.migrate_item_sources(item_id)
        await self.migrate_item_providers(item_id)
        await self.migrate_file_images(item_id)
        
        # 显示统计
        print(f"\n{'='*60}")
        print("迁移完成统计")
        print(f"{'='*60}")
        for key, count in self.stats.items():
            print(f"  {key:20s}: {count:4d}")
        
        total = sum(self.stats.values())
        print(f"  {'总计':20s}: {total:4d}")
        
        return True


async def main():
    if len(sys.argv) < 2:
        print("用法: python migrate_item_associations.py <item_id>")
        print("示例: python migrate_item_associations.py 100")
        sys.exit(1)
    
    item_id = int(sys.argv[1])
    
    # 连接远程数据库
    print("🔗 连接远程 PostgreSQL...")
    remote_conn = await asyncpg.connect(**REMOTE_DB_CONFIG)
    print("✅ 连接成功")
    
    # 创建本地会话
    async with AsyncSessionLocal() as local_session:
        migrator = AssociationMigrator(remote_conn, local_session)
        success = await migrator.migrate_all(item_id)
    
    await remote_conn.close()
    
    if success:
        print("\n✅ 伴生属性迁移完成！")
    else:
        print("\n❌ 迁移失败")
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
