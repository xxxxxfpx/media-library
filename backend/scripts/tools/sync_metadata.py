"""
同步 Genre/Tag/Studio 元数据
确保关联的 MediaItems 正确
"""
import os
import asyncio
import asyncpg
from database.core import AsyncSessionLocal, engine
from database.models import MediaItem, MediaType
from sqlalchemy import select, delete

REMOTE_DB_CONFIG = {
    'host': os.environ.get('REMOTE_DB_HOST', ''),
    'port': int(os.environ.get('REMOTE_DB_PORT', '5432')),
    'database': os.environ.get('REMOTE_DB_NAME', ''),
    'user': os.environ.get('REMOTE_DB_USER', ''),
    'password': os.environ.get('REMOTE_DB_PASSWORD', '')
}


async def sync_metadata():
    """同步 Genre/Tag/Studio 数据"""
    remote_conn = await asyncpg.connect(**REMOTE_DB_CONFIG)
    
    async with AsyncSessionLocal() as session:
        # 获取 ID=3102 关联的所有 Genre/Tag/Studio
        linked_items = await remote_conn.fetch(
            '''SELECT DISTINCT mi."Id", mi."Type", mi."Name"
               FROM "ItemLinks" il
               JOIN "MediaItems" mi ON il."LinkedItemId" = mi."Id"
               WHERE il."ItemId" = $1 
               AND mi."Type" IN ('Genre', 'Tag', 'Studio', 'BoxSet')''',
            3102
        )
        
        print(f"需要同步 {len(linked_items)} 个元数据项:\n")
        
        type_map = {
            'Genre': MediaType.Genre,
            'Tag': MediaType.Tag,
            'Studio': MediaType.Studio,
            'BoxSet': MediaType.BoxSet,
        }
        
        for item in linked_items:
            remote_type = item['Type']
            local_type = type_map.get(remote_type)
            
            if not local_type:
                continue
            
            # 检查本地是否已存在
            result = await session.execute(
                select(MediaItem).where(MediaItem.Id == item['Id'])
            )
            existing = result.scalar_one_or_none()
            
            if existing:
                if existing.Type != local_type or existing.Name != item['Name']:
                    print(f"  更新 ID={item['Id']}: {existing.Name} ({existing.Type}) -> {item['Name']} ({local_type})")
                    existing.Type = local_type
                    existing.Name = item['Name']
                else:
                    print(f"  已存在 ID={item['Id']}: {item['Name']} ({local_type})")
            else:
                print(f"  创建 ID={item['Id']}: {item['Name']} ({local_type})")
                new_item = MediaItem(
                    Id=item['Id'],
                    Type=local_type,
                    Name=item['Name'],
                    IsDeleted=False,
                )
                session.add(new_item)
        
        await session.commit()
        print("\n✅ 元数据同步完成!")
    
    await remote_conn.close()


if __name__ == '__main__':
    asyncio.run(sync_metadata())
