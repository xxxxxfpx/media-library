"""
检查远程数据库中 ItemLinks 关联项的类型
"""
import os
import asyncio
import asyncpg

REMOTE_DB_CONFIG = {
    'host': os.environ.get('REMOTE_DB_HOST', ''),
    'port': int(os.environ.get('REMOTE_DB_PORT', '5432')),
    'database': os.environ.get('REMOTE_DB_NAME', ''),
    'user': os.environ.get('REMOTE_DB_USER', ''),
    'password': os.environ.get('REMOTE_DB_PASSWORD', '')
}

async def check():
    conn = await asyncpg.connect(**REMOTE_DB_CONFIG)
    
    # 获取 ID=3102 的所有关联
    print("检查 ItemId=3102 的关联项类型:\n")
    
    links = await conn.fetch(
        '''SELECT il."LinkedItemId", mi."Type", mi."Name"
           FROM "ItemLinks" il
           JOIN "MediaItems" mi ON il."LinkedItemId" = mi."Id"
           WHERE il."ItemId" = $1
           ORDER BY mi."Type"''',
        3102
    )
    
    type_count = {}
    for link in links:
        t = link['Type']
        type_count[t] = type_count.get(t, 0) + 1
        print(f"  {link['Type']:15} | ID={link['LinkedItemId']:5} | {link['Name'][:30]}")
    
    print(f"\n类型统计:")
    for t, count in sorted(type_count.items()):
        print(f"  {t}: {count}")
    
    await conn.close()

asyncio.run(check())
