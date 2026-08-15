"""验证迁移完整性 - 检查哪些 Movie 缺失"""
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
    
    # 获取远程所有 Hanime Movie IDs
    remote_movies = await conn.fetch('''
        SELECT mi."Id" FROM "MediaItems" mi
        JOIN "ItemProviders" ip ON mi."Id" = ip."ItemId"
        WHERE mi."Type" = 'Movie' AND ip."ProviderId" = 1
    ''')
    remote_ids = {r['Id'] for r in remote_movies}
    print(f'远程 Hanime Movie 数量: {len(remote_ids)}')
    
    # 查询本地数据库
    from database.core import AsyncSessionLocal
    from database.models import MediaItem
    from sqlalchemy import select
    
    async with AsyncSessionLocal() as s:
        result = await s.execute(select(MediaItem.Id).where(MediaItem.Type == 'Movie'))
        local_ids = {row[0] for row in result.all()}
        print(f'本地 Movie 数量: {len(local_ids)}')
        
        missing = remote_ids - local_ids
        print(f'\n缺失 Movie 数量: {len(missing)}')
        
        # 随机显示一些缺失的 ID
        print(f'\n前10个缺失的 Movie ID:')
        for mid in list(missing)[:10]:
            # 查询远程该 Movie 的信息
            info = await conn.fetchrow('SELECT "Id", "Name", "Type" FROM "MediaItems" WHERE "Id" = $1', mid)
            print(f'  Id={info["Id"]}, Name={info["Name"]}')
    
    await conn.close()


asyncio.run(check())
