import os
import asyncio
import asyncpg

async def check_providers():
    conn = await asyncpg.connect(host=os.environ.get('REMOTE_DB_HOST', ''), port=int(os.environ.get('REMOTE_DB_PORT', '5432')), database=os.environ.get('REMOTE_DB_NAME', ''), user=os.environ.get('REMOTE_DB_USER', ''), password=os.environ.get('REMOTE_DB_PASSWORD', ''))
    rows = await conn.fetch('SELECT * FROM "Providers" LIMIT 10')
    print('Providers 表数据:')
    for row in rows:
        print(dict(row))
    await conn.close()

asyncio.run(check_providers())
