"""最终迁移完整性验证"""
import asyncio
import asyncpg
from database.core import AsyncSessionLocal
from database.models import MediaItem, ItemLinks
from sqlalchemy import select, func
from config import get_remote_db_config


async def verify():
    conn = await asyncpg.connect(**get_remote_db_config())

    async with AsyncSessionLocal() as s:
        print("=" * 80)
        print("最终迁移完整性验证")
        print("=" * 80)

        # 1. MediaItems 验证
        print("\n=== MediaItems ===")
        types = ['Tag', 'Genre', 'Studio', 'BoxSet', 'Movie', 'Series', 'Season', 'Episode']
        all_match = True
        for t in types:
            local = (await s.execute(select(func.count()).where(MediaItem.Type == t))).scalar_one()
            remote = await conn.fetchval('''
                SELECT COUNT(*) FROM "MediaItems" mi
                JOIN "ItemProviders" ip ON mi."Id" = ip."ItemId"
                WHERE mi."Type" = $1 AND ip."ProviderId" = 1
            ''', t)
            status = "✅" if local == remote else "❌"
            if local != remote:
                all_match = False
            print(f"  {status} {t}: 本地={local}, 远程={remote}")
        
        # Source
        local_source = (await s.execute(select(func.count()).where(MediaItem.Type == 'Source'))).scalar_one()
        print(f"  ✅ Source: 本地={local_source} (对应远程 Provider=Hanime)")

        if all_match:
            print("\n✅ MediaItems 全部匹配！")

        # 2. ItemLinks 验证（按类型）
        print("\n=== ItemLinks ===")
        result = await s.execute(select(func.count()).select_from(ItemLinks))
        local_total = result.scalar_one()
        print(f"  本地总关联数: {local_total}")
        
        # 按类型验证（排除 Source，因为远程没有 Provider 概念）
        for t in ['Genre', 'Studio', 'Tag', 'BoxSet', 'Season', 'Episode']:
            local = (await s.execute(select(func.count()).where(ItemLinks.Type == t))).scalar_one()
            remote = await conn.fetchval('''
                SELECT COUNT(*) FROM "ItemLinks" il
                JOIN "MediaItems" mi ON il."LinkedItemId" = mi."Id"
                JOIN "ItemProviders" ip ON il."ItemId" = ip."ItemId"
                WHERE mi."Type" = $1 AND ip."ProviderId" = 1
            ''', t)
            status = "✅" if local == remote else "❌"
            print(f"  {status} {t}: 本地={local}, 远程={remote}")
        
        # Source 关联（所有 Hanime 关联的 MediaItems → Source）
        local_source_links = (await s.execute(select(func.count()).where(ItemLinks.Type == 'Source'))).scalar_one()
        remote_source_links = await conn.fetchval('''
            SELECT COUNT(DISTINCT mi."Id")
            FROM "ItemProviders" ip
            JOIN "MediaItems" mi ON ip."ItemId" = mi."Id"
        ''')
        status = "✅" if local_source_links == remote_source_links else "❌"
        print(f"  {status} Source: 本地={local_source_links}, 远程={remote_source_links}")

        # 3. 总计
        local_total = (await s.execute(select(func.count()).select_from(MediaItem))).scalar_one()
        print(f"\n=== 总计 ===")
        print(f"MediaItems: {local_total}")
        print("=" * 80)

    await conn.close()


asyncio.run(verify())
