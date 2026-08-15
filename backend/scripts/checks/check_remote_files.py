"""检查远程数据库文件表结构"""
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
    
    # 查询远程文件表结构
    columns = await conn.fetch('''
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = 'Files'
        ORDER BY ordinal_position
    ''')
    print('远程 Files 表结构:')
    for col in columns:
        print(f'  {col["column_name"]}: {col["data_type"]}')
    
    # 查询远程文件数量
    total_files = await conn.fetchval('SELECT COUNT(*) FROM "Files"')
    print(f'\n远程 Files 总数: {total_files}')
    
    # 查询 Hanime 关联的文件数量
    hanime_files = await conn.fetchval('''
        SELECT COUNT(DISTINCT f."Id")
        FROM "Files" f
        JOIN "FileImages" fi ON f."Id" = fi."FileId"
        JOIN "ItemProviders" ip ON fi."ItemId" = ip."ItemId"
        WHERE ip."ProviderId" = 1
    ''')
    print(f'Hanime 关联的图片文件: {hanime_files}')
    
    # 查询 ItemSources (视频文件)
    sources = await conn.fetchval('''
        SELECT COUNT(DISTINCT s."ItemId")
        FROM "ItemSources" s
        JOIN "ItemProviders" ip ON s."ItemId" = ip."ItemId"
        WHERE ip."ProviderId" = 1
    ''')
    print(f'Hanime 关联的视频源: {sources}')
    
    # 查看 FileImages 表结构
    fi_columns = await conn.fetch('''
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = 'FileImages'
        ORDER BY ordinal_position
    ''')
    print('\n远程 FileImages 表结构:')
    for col in fi_columns:
        print(f'  {col["column_name"]}: {col["data_type"]}')
    
    # 查看 ItemSources 表结构
    is_columns = await conn.fetch('''
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = 'ItemSources'
        ORDER BY ordinal_position
    ''')
    print('\n远程 ItemSources 表结构:')
    for col in is_columns:
        print(f'  {col["column_name"]}: {col["data_type"]}')
    
    # 查看示例数据
    sample_files = await conn.fetch('SELECT * FROM "Files" LIMIT 3')
    print('\nFiles 示例数据:')
    for row in sample_files:
        print(f'  Id={row["Id"]}, Path={row["Path"][:50]}..., Type={row["Type"]}')
    
    await conn.close()


asyncio.run(check())
