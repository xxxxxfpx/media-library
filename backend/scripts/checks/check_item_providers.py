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
    
    # 检查 ItemProviders 表中 ItemId=3102 的数据
    rows = await conn.fetch(
        'SELECT * FROM "ItemProviders" WHERE "ItemId" = $1',
        3102
    )
    print(f"ItemProviders for ItemId=3102: {len(rows)} rows")
    for row in rows:
        print(f"  {dict(row)}")
    
    await conn.close()

asyncio.run(check())
