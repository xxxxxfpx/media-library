"""补全缺失的关联关系 - 优化版"""
import os
import asyncio
import asyncpg
from database.core import AsyncSessionLocal
from database.models import ItemLinks
from sqlalchemy import select


async def fill_missing_links():
    conn = await asyncpg.connect(
        host=os.environ.get('REMOTE_DB_HOST', ''),
        port=int(os.environ.get('REMOTE_DB_PORT', '5432')),
        database=os.environ.get('REMOTE_DB_NAME', ''),
        user=os.environ.get('REMOTE_DB_USER', ''),
        password=os.environ.get('REMOTE_DB_PASSWORD', '')
    )

    async with AsyncSessionLocal() as s:
        for link_type in ['Studio', 'Tag', 'BoxSet']:
            print(f"\n=== 补全 {link_type} 关联 ===")
            
            # 批量获取远程关联
            remote_links = await conn.fetch('''
                SELECT il."ItemId", il."LinkedItemId"
                FROM "ItemLinks" il
                JOIN "ItemProviders" ip ON il."ItemId" = ip."ItemId"
                JOIN "MediaItems" mi ON il."LinkedItemId" = mi."Id"
                WHERE mi."Type" = $1 AND ip."ProviderId" = 1
            ''', link_type)
            print(f"远程 {link_type} 关联总数: {len(remote_links)}")
            
            # 批量获取本地已有
            result = await s.execute(select(ItemLinks.ItemId, ItemLinks.LinkedItemId).where(ItemLinks.Type == link_type))
            existing = {(row.ItemId, row.LinkedItemId) for row in result.all()}
            print(f"本地已有: {len(existing)}")
            
            # 找出缺失的
            missing = [(r['ItemId'], r['LinkedItemId']) for r in remote_links 
                      if (r['ItemId'], r['LinkedItemId']) not in existing]
            print(f"需要补全: {len(missing)}")
            
            # 批量插入
            created = 0
            for item_id, linked_id in missing:
                link = ItemLinks(
                    ItemId=item_id,
                    LinkedItemId=linked_id,
                    Type=link_type,
                )
                s.add(link)
                created += 1
                if created % 1000 == 0:
                    await s.commit()
                    print(f"  已插入 {created}/{len(missing)}")
            
            await s.commit()
            print(f"✅ 补全 {created} 个 {link_type} 关联")

        # 补全 Source 关联
        print("\n=== 补全 Source 关联 ===")
        remote_source_items = await conn.fetch('''
            SELECT DISTINCT mi."Id"
            FROM "ItemProviders" ip
            JOIN "MediaItems" mi ON ip."ItemId" = mi."Id"
        ''')
        print(f"需要 Source 关联的项: {len(remote_source_items)}")
        
        # 获取本地已有
        result = await s.execute(select(ItemLinks.ItemId).where(
            ItemLinks.LinkedItemId == 1,
            ItemLinks.Type == 'Source'
        ))
        existing_source = {row.ItemId for row in result.all()}
        
        missing_source = [r['Id'] for r in remote_source_items if r['Id'] not in existing_source]
        print(f"需要补全: {len(missing_source)}")
        
        created = 0
        for item_id in missing_source:
            link = ItemLinks(
                ItemId=item_id,
                LinkedItemId=1,
                Type='Source',
            )
            s.add(link)
            created += 1
            if created % 1000 == 0:
                await s.commit()
                print(f"  已插入 {created}/{len(missing_source)}")
        
        await s.commit()
        print(f"✅ 补全 {created} 个 Source 关联")

    await conn.close()
    print("\n✅ 所有关联关系补全完成！")


asyncio.run(fill_missing_links())
