"""
迁移 Source 来源数据
1. Providers → Source 类型 MediaItems
2. ItemProviders → ItemLinks (Type=Source)
"""
import os
import asyncio
import asyncpg
from datetime import datetime
from database.core import AsyncSessionLocal
from database.models import MediaItem, MediaType, ItemLinks, ItemLinkType
from sqlalchemy import select

REMOTE_DB_CONFIG = {
    'host': os.environ.get('REMOTE_DB_HOST', ''),
    'port': int(os.environ.get('REMOTE_DB_PORT', '5432')),
    'database': os.environ.get('REMOTE_DB_NAME', ''),
    'user': os.environ.get('REMOTE_DB_USER', ''),
    'password': os.environ.get('REMOTE_DB_PASSWORD', '')
}


async def migrate_sources():
    """迁移 Providers 为 Source 类型的 MediaItems"""
    print("迁移 Providers → Source...")
    
    remote_conn = await asyncpg.connect(**REMOTE_DB_CONFIG)
    
    async with AsyncSessionLocal() as session:
        # 获取所有 Providers
        providers = await remote_conn.fetch(
            'SELECT "Id", "Name", "Url", "Description" FROM "Providers"'
        )
        
        provider_id_map = {}  # 旧 ProviderId -> 新 MediaItem Id
        
        for p in providers:
            # 检查是否已存在
            result = await session.execute(
                select(MediaItem).where(
                    MediaItem.Name == p['Name'],
                    MediaItem.Type == MediaType.Source
                )
            )
            existing = result.scalar_one_or_none()
            
            if existing:
                provider_id_map[p['Id']] = existing.Id
                print(f"  已存在: {p['Name']} (ID={existing.Id})")
            else:
                # 创建 Source 类型的 MediaItem
                source = MediaItem(
                    Type=MediaType.Source,
                    Name=p['Name'],
                    Overview=p['Description'] or f"来自 {p['Name']}",
                    IsDeleted=False,
                    DateCreated=datetime.utcnow(),
                    DateModified=datetime.utcnow(),
                )
                session.add(source)
                await session.flush()
                provider_id_map[p['Id']] = source.Id
                print(f"  创建: {p['Name']} (ID={source.Id})")
        
        await session.commit()
        
        # 迁移 ItemProviders 为 ItemLinks
        print("\n迁移 ItemProviders → ItemLinks...")
        
        # 获取指定视频的 ItemProviders
        item_providers = await remote_conn.fetch(
            'SELECT "ItemId", "ProviderId" FROM "ItemProviders" WHERE "ItemId" = $1',
            3102
        )
        
        for ip in item_providers:
            provider_id = ip['ProviderId']
            media_item_id = provider_id_map.get(provider_id)
            
            if media_item_id:
                # 检查是否已存在
                result = await session.execute(
                    select(ItemLinks).where(
                        ItemLinks.ItemId == ip['ItemId'],
                        ItemLinks.LinkedItemId == media_item_id,
                        ItemLinks.Type == ItemLinkType.Source
                    )
                )
                if not result.scalar_one_or_none():
                    link = ItemLinks(
                        ItemId=ip['ItemId'],
                        LinkedItemId=media_item_id,
                        Type=ItemLinkType.Source,
                    )
                    session.add(link)
                    print(f"  添加 Source 关联: Item {ip['ItemId']} -> Source {media_item_id}")
        
        await session.commit()
    
    await remote_conn.close()
    print("\n✅ Source 迁移完成！")


if __name__ == '__main__':
    asyncio.run(migrate_sources())
