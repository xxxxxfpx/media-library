"""
清理并重新迁移 ID=3102 的 ItemLinks
根据远程数据库正确的类型映射
"""
import os
import asyncio
import asyncpg
from database.core import AsyncSessionLocal, engine
from database.models import ItemLinks, ItemLinkType
from sqlalchemy import delete, select
from datetime import datetime

REMOTE_DB_CONFIG = {
    'host': os.environ.get('REMOTE_DB_HOST', ''),
    'port': int(os.environ.get('REMOTE_DB_PORT', '5432')),
    'database': os.environ.get('REMOTE_DB_NAME', ''),
    'user': os.environ.get('REMOTE_DB_USER', ''),
    'password': os.environ.get('REMOTE_DB_PASSWORD', '')
}

# 类型映射
TYPE_MAP = {
    'Genre': ItemLinkType.Genre,
    'Tag': ItemLinkType.Tag,
    'Studio': ItemLinkType.Studio,
    'BoxSet': ItemLinkType.BoxSet,
}


async def clean_and_migrate():
    remote_conn = await asyncpg.connect(**REMOTE_DB_CONFIG)
    
    async with AsyncSessionLocal() as session:
        # 1. 清理 ID=3102 的所有 ItemLinks
        print("清理 ID=3102 的所有 ItemLinks...")
        result = await session.execute(
            delete(ItemLinks).where(ItemLinks.ItemId == 3102)
        )
        await session.commit()
        print(f"  ✅ 已清理")
        
        # 2. 获取远程正确的关联数据
        print("\n获取远程正确的关联数据...")
        links = await remote_conn.fetch(
            '''SELECT il."LinkedItemId", mi."Type", mi."Name"
               FROM "ItemLinks" il
               JOIN "MediaItems" mi ON il."LinkedItemId" = mi."Id"
               WHERE il."ItemId" = $1''',
            3102
        )
        
        print(f"  发现 {len(links)} 条关联")
        
        # 3. 按类型分类并迁移
        type_count = {}
        for link in links:
            remote_type = link['Type']
            local_type = TYPE_MAP.get(remote_type)
            
            if not local_type:
                print(f"  ⚠️ 跳过未知类型: {remote_type}")
                continue
            
            # 创建 ItemLinks
            item_link = ItemLinks(
                ItemId=3102,
                LinkedItemId=link['LinkedItemId'],
                Type=local_type,
            )
            session.add(item_link)
            
            type_count[remote_type] = type_count.get(remote_type, 0) + 1
        
        await session.commit()
        
        print("\n✅ 迁移完成统计:")
        for t, count in sorted(type_count.items()):
            print(f"  {t}: {count}")
    
    await remote_conn.close()


if __name__ == '__main__':
    asyncio.run(clean_and_migrate())
