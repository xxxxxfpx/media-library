"""检查远程数据库 Cosplay 的情况"""
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

    # 查找所有名为 Cosplay 的项
    rows = await conn.fetch('SELECT "Id", "Type", "Name" FROM "MediaItems" WHERE "Name" = $1', 'Cosplay')
    print('远程数据库 Cosplay:')
    for r in rows:
        print(f'  Id={r["Id"]}, Type={r["Type"]}, Name={r["Name"]}')

    await conn.close()


asyncio.run(check())
