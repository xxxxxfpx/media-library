"""验证迁移完整性 - 检查缺失原因"""
import os
import asyncio
import asyncpg


async def check():
    conn = await asyncpg.connect(
        host=os.environ.get('REMOTE_DB_HOST', ''),
        port=int(os.environ.get('REMOTE_DB_PORT', '5432')),
        database=os.environ.get('REMOTE_DB_NAME', ''),
        user=os.environ.get('REMOTE_DB_USER', ''),
        password=os.environ.get('REMOTE_DB_PASSWORD', '')
    )
    
    from database.core import AsyncSessionLocal
    from database.models import MediaItem
    from sqlalchemy import select
    
    async with AsyncSessionLocal() as s:
        # 1. 检查缺失的 Studio
        remote_studios = await conn.fetch('''
            SELECT mi."Id", mi."Name"
            FROM "MediaItems" mi
            JOIN "ItemProviders" ip ON mi."Id" = ip."ItemId"
            WHERE mi."Type" = 'Studio' AND ip."ProviderId" = 1
        ''')
        
        result = await s.execute(select(MediaItem.Id, MediaItem.Name).where(MediaItem.Type == 'Studio'))
        local_studios = {row.Name: row.Id for row in result.all()}
        
        missing_studios = []
        for studio in remote_studios:
            if studio['Name'] in local_studios:
                continue
            missing_studios.append(studio)
        
        print(f"Studio: 远程={len(remote_studios)}, 本地={len(local_studios)}, 缺失={len(missing_studios)}")
        if missing_studios:
            print("  缺失示例:")
            for s in missing_studios[:5]:
                print(f"    Id={s['Id']}, Name={s['Name']}")
        
        # 检查是否有同名但不同 ID 的情况
        name_counts = {}
        for studio in remote_studios:
            if studio['Name'] not in name_counts:
                name_counts[studio['Name']] = []
            name_counts[studio['Name']].append(studio)
        
        duplicates = {name: items for name, items in name_counts.items() if len(items) > 1}
        print(f"  远程有重复名称的 Studio: {len(duplicates)} 个")
        for name, items in list(duplicates.items())[:3]:
            ids = [item['Id'] for item in items]
            print(f"    '{name}': IDs={ids}")
    
    await conn.close()


asyncio.run(check())
