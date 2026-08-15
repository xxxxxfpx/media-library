"""验证所有 Item 和 File 是否正确迁移"""
import os
import asyncio
import asyncpg
from database.core import AsyncSessionLocal
from database.models import MediaItem, File, FileLink
from sqlalchemy import select, func


async def verify_all():
    conn = await asyncpg.connect(
        host=os.environ.get('REMOTE_DB_HOST', ''),
        port=int(os.environ.get('REMOTE_DB_PORT', '5432')),
        database=os.environ.get('REMOTE_DB_NAME', ''),
        user=os.environ.get('REMOTE_DB_USER', ''),
        password=os.environ.get('REMOTE_DB_PASSWORD', '')
    )

    async with AsyncSessionLocal() as s:
        print("="*80)
        print("完整迁移验证报告")
        print("="*80)

        # 1. 验证 MediaItems
        print("\n=== MediaItems 验证 ===")
        
        # 远程没有 Source 类型，本地 Source 对应远程的 Provider
        local_source = (await s.execute(
            select(func.count()).where(MediaItem.Type == 'Source')
        )).scalar_one()
        print(f"  Source: 本地={local_source} (对应远程 Provider=Hanime)")
        
        types = ['Tag', 'Genre', 'Studio', 'BoxSet', 'Movie', 'Series', 'Season', 'Episode']
        for t in types:
            local_count = (await s.execute(
                select(func.count()).where(MediaItem.Type == t)
            )).scalar_one()
            
            remote_count = await conn.fetchval('''
                SELECT COUNT(*) FROM "MediaItems" mi
                JOIN "ItemProviders" ip ON mi."Id" = ip."ItemId"
                WHERE mi."Type" = $1 AND ip."ProviderId" = 1
            ''', t)
            print(f"  {t}: 本地={local_count}, 远程={remote_count}")
            
            if local_count != remote_count:
                print(f"    ⚠️ 差异: {local_count - remote_count}")

        # 2. 验证 ItemLinks
        print("\n=== ItemLinks 验证 ===")
        
        # 本地总关联数
        local_links = (await s.execute(select(func.count(ItemLinks)))).scalar_one()
        print(f"  本地总关联数: {local_links}")
        
        # 按类型统计
        for link_type in ['Source', 'Genre', 'Studio', 'Tag', 'BoxSet', 'Season', 'Episode']:
            local_type = (await s.execute(
                select(func.count()).where(ItemLinks.Type == link_type)
            )).scalar_one()
            
            remote_type_lower = link_type.lower()
            if link_type == 'Source':
                # Source 关联：所有 Hanime 关联的 MediaItems → Source
                remote_type = await conn.fetchval('''
                    SELECT COUNT(DISTINCT mi."Id")
                    FROM "ItemProviders" ip
                    JOIN "MediaItems" mi ON ip."ItemId" = mi."Id"
                ''')
                print(f"  {link_type}: 本地={local_type}, 远程={remote_type}")
            else:
                remote_type = await conn.fetchval('''
                    SELECT COUNT(*) FROM "ItemLinks" il
                    JOIN "MediaItems" mi ON il."LinkedItemId" = mi."Id"
                    JOIN "ItemProviders" ip ON il."ItemId" = ip."ItemId"
                    WHERE mi."Type" = $1 AND ip."ProviderId" = 1
                ''', remote_type_lower)
                print(f"  {link_type}: 本地={local_type}, 远程={remote_type}")
            
            if local_type != remote_type:
                print(f"    ⚠️ 差异: {local_type - remote_type}")

        # 3. 验证 Files
        print("\n=== Files 验证 ===")
        local_files = (await s.execute(select(func.count(File)))).scalar_one()
        local_filelinks = (await s.execute(select(func.count(FileLink)))).scalar_one()
        print(f"  本地 File 数量: {local_files}")
        print(f"  本地 FileLink 数量: {local_filelinks}")
        print("  注意: 本次迁移未迁移 File 和 FileLink 数据")

        # 4. 总结
        print("\n" + "="*80)
        local_total = (await s.execute(select(func.count(MediaItem)))).scalar_one()
        print(f"MediaItems 总计: {local_total}")
        print("="*80)

    await conn.close()


asyncio.run(verify_all())
