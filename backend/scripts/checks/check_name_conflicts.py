"""检查 Studio 和 BoxSet 的 Name 冲突"""
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
    
    # 1. 检查 Studio 名称冲突
    studios = await conn.fetch('''
        SELECT mi."Id", mi."Name", mi."Type"
        FROM "MediaItems" mi
        JOIN "ItemProviders" ip ON mi."Id" = ip."ItemId"
        WHERE mi."Type" = 'Studio' AND ip."ProviderId" = 1
    ''')
    
    # 查找重复名称
    from collections import Counter
    name_counter = Counter([r['Name'] for r in studios])
    duplicates = {name: count for name, count in name_counter.items() if count > 1}
    
    print(f"远程 Studio 总数: {len(studios)}")
    print(f"有重复名称的 Studio: {len(duplicates)} 个")
    if duplicates:
        print("重复示例:")
        for name, count in list(duplicates.items())[:5]:
            print(f"  '{name}': {count} 次")
    
    # 2. 检查 BoxSet 名称冲突
    boxsets = await conn.fetch('''
        SELECT mi."Id", mi."Name", mi."Type"
        FROM "MediaItems" mi
        JOIN "ItemProviders" ip ON mi."Id" = ip."ItemId"
        WHERE mi."Type" = 'BoxSet' AND ip."ProviderId" = 1
    ''')
    
    name_counter2 = Counter([r['Name'] for r in boxsets])
    duplicates2 = {name: count for name, count in name_counter2.items() if count > 1}
    
    print(f"\n远程 BoxSet 总数: {len(boxsets)}")
    print(f"有重复名称的 BoxSet: {len(duplicates2)} 个")
    if duplicates2:
        print("重复示例:")
        for name, count in list(duplicates2.items())[:5]:
            print(f"  '{name}': {count} 次")
    
    # 3. 检查 Movie 名称冲突
    movies = await conn.fetch('''
        SELECT mi."Id", mi."Name", mi."Type"
        FROM "MediaItems" mi
        JOIN "ItemProviders" ip ON mi."Id" = ip."ItemId"
        WHERE mi."Type" = 'Movie' AND ip."ProviderId" = 1
    ''')
    
    name_counter3 = Counter([r['Name'] for r in movies])
    duplicates3 = {name: count for name, count in name_counter3.items() if count > 1}
    
    print(f"\n远程 Movie 总数: {len(movies)}")
    print(f"有重复名称的 Movie: {len(duplicates3)} 个")
    if duplicates3:
        print("重复示例:")
        for name, count in list(duplicates3.items())[:5]:
            print(f"  '{name}': {count} 次")
    
    await conn.close()


asyncio.run(check())
