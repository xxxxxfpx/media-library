"""查询远程数据库 Hanime Provider 的 Genre 数量"""
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

    # 查询 Hanime Provider 关联的 Genre 数量
    count = await conn.fetchval(
        'SELECT COUNT(*) FROM "ItemProviders" ip JOIN "MediaItems" mi ON ip."ItemId" = mi."Id" WHERE ip."ProviderId" = $1 AND mi."Type" = $2',
        1, 'Genre'
    )
    print(f'Hanime Provider 关联的 Genre 数量: {count}')

    # 查询 Genre 列表
    rows = await conn.fetch(
        'SELECT mi."Id", mi."Name" FROM "ItemProviders" ip JOIN "MediaItems" mi ON ip."ItemId" = mi."Id" WHERE ip."ProviderId" = $1 AND mi."Type" = $2',
        1, 'Genre'
    )
    print('\nGenre 列表:')
    for r in rows:
        print(f'  Id={r["Id"]}, Name={r["Name"]}')

    # 查询远程总 Genre 数量
    total = await conn.fetchval('SELECT COUNT(*) FROM "MediaItems" WHERE "Type" = $1', 'Genre')
    print(f'\n远程数据库总 Genre 数量: {total}')

    # 查询前20个Genre
    rows2 = await conn.fetch('SELECT "Id", "Name" FROM "MediaItems" WHERE "Type" = $1 LIMIT 20', 'Genre')
    print('前20个 Genre:')
    for r in rows2:
        print(f'  Id={r["Id"]}, Name={r["Name"]}')

    await conn.close()


asyncio.run(check())
