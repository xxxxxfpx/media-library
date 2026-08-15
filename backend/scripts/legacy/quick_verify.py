"""快速验证迁移完整性"""
import os
import asyncio
import asyncpg
from database.core import AsyncSessionLocal
from database.models import MediaItem, ItemLinks
from sqlalchemy import select, func


async def verify():
    conn = await asyncpg.connect(
        host=os.environ.get('REMOTE_DB_HOST', ''),
        port=int(os.environ.get('REMOTE_DB_PORT', '5432')),
        database=os.environ.get('REMOTE_DB_NAME', ''),
        user=os.environ.get('REMOTE_DB_USER', ''),
        password=os.environ.get('REMOTE_DB_PASSWORD', '')
    )

    async with AsyncSessionLocal() as s:
        print("=" * 80)
        print("迁移完整性验证")
        print("=" * 80)

        # 1. MediaItems 验证
        print("\n=== MediaItems ===")
        types = ['Tag', 'Genre', 'Studio', 'BoxSet', 'Movie', 'Series', 'Season', 'Episode']
        for t in types:
            local = (await s.execute(select(func.count()).where(MediaItem.Type == t))).scalar_one()
            remote = await conn.fetchval('''
                SELECT COUNT(*) FROM "MediaItems" mi
                JOIN "ItemProviders" ip ON mi."Id" = ip."ItemId"
                WHERE mi."Type" = $1 AND ip."ProviderId" = 1
            ''', t)
            status = "✅" if local == remote else "❌"
            print(f"  {status} {t}: 本地={local}, 远程={remote}")

        # 2. 总关联数验证
        print("\n=== ItemLinks ===")
        result = await s.execute(select(func.count()).select_from(ItemLinks))
        local_total = result.scalar_one()
        print(f"  本地总关联数: {local_total}")
        
        # 按类型验证
        for t in ['Source', 'Genre', 'Studio', 'Tag', 'BoxSet', 'Season', 'Episode']:
            local = (await s.execute(select(func.count()).where(ItemLinks.Type == t))).scalar_one()
            remote = await conn.fetchval('''
                SELECT COUNT(*) FROM "ItemLinks" il
                JOIN "MediaItems" mi ON il."LinkedItemId" = mi."Id"
                JOIN "ItemProviders" ip ON il."ItemId" = ip."ItemId"
                WHERE mi."Type" = $1 AND ip."ProviderId" = 1
            ''', t)
            status = "✅" if local == remote else "❌"
            print(f"  {status} {t}: 本地={local}, 远程={remote}")

        # 3. 本地总记录数
        local_total = (await s.execute(select(func.count(MediaItem)))).scalar_one()
        print(f"\n本地 MediaItems 总计: {local_total}")
        print("=" * 80)

    await conn.close()


asyncio.run(verify())
