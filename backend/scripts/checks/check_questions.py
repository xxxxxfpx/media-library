"""检查远程数据库的关键问题"""
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
    
    print("=" * 80)
    print("问题 1: 检查 Season 和 Episode 的 parent_id 字段")
    print("=" * 80)
    
    # 检查 Season 的 parent_id
    season_rows = await conn.fetch('''
        SELECT "Id", "Name", "ParentId" 
        FROM "MediaItems" 
        WHERE "Type" = 'Season' 
        LIMIT 5
    ''')
    print("\nSeason 示例:")
    for r in season_rows:
        print(f"  Id={r['Id']}, Name={r['Name']}, ParentId={r['ParentId']}")
        if r['ParentId']:
            parent = await conn.fetchrow('SELECT "Name", "Type" FROM "MediaItems" WHERE "Id" = $1', r['ParentId'])
            if parent:
                print(f"    → Parent: {parent['Name']} ({parent['Type']})")
    
    # 检查 Episode 的 parent_id
    episode_rows = await conn.fetch('''
        SELECT "Id", "Name", "ParentId" 
        FROM "MediaItems" 
        WHERE "Type" = 'Episode' 
        LIMIT 5
    ''')
    print("\nEpisode 示例:")
    for r in episode_rows:
        print(f"  Id={r['Id']}, Name={r['Name']}, ParentId={r['ParentId']}")
        if r['ParentId']:
            parent = await conn.fetchrow('SELECT "Name", "Type" FROM "MediaItems" WHERE "Id" = $1', r['ParentId'])
            if parent:
                print(f"    → Parent: {parent['Name']} ({parent['Type']})")
    
    print("\n" + "=" * 80)
    print("问题 2: 检查 BoxSet 的关联关系")
    print("=" * 80)
    
    boxset_rows = await conn.fetch('''
        SELECT "Id", "Name" FROM "MediaItems" 
        WHERE "Type" = 'BoxSet' 
        LIMIT 3
    ''')
    for boxset in boxset_rows:
        print(f"\nBoxSet: {boxset['Id']} - {boxset['Name']}")
        links = await conn.fetch('''
            SELECT il."LinkedItemId", mi."Name", mi."Type"
            FROM "ItemLinks" il
            JOIN "MediaItems" mi ON il."LinkedItemId" = mi."Id"
            WHERE il."ItemId" = $1
            LIMIT 5
        ''', boxset['Id'])
        print(f"  关联项数量：{len(links)}")
        for l in links:
            print(f"    - {l['LinkedItemId']}: {l['Name']} ({l['Type']})")
    
    print("\n" + "=" * 80)
    print("问题 3: 检查远程数据库的 MediaItems 类型分布")
    print("=" * 80)
    
    # 检查所有类型分布
    type_dist = await conn.fetch('''
        SELECT "Type", COUNT(*) as cnt
        FROM "MediaItems"
        GROUP BY "Type"
        ORDER BY cnt DESC
    ''')
    print(f"\n远程数据库 MediaItems 类型分布:")
    for t in type_dist:
        print(f"  {t['Type']}: {t['cnt']}")
    
    print("\n" + "=" * 80)
    print("问题 4: 检查远程 ItemLinks 表结构")
    print("=" * 80)
    
    # 检查 ItemLinks 表结构
    cols = await conn.fetch('''
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = 'itemlinks'
        ORDER BY ordinal_position
    ''')
    print(f"\nItemLinks 表结构:")
    for c in cols:
        print(f"  {c['column_name']}: {c['data_type']}")
    
    # 检查 ItemLinks 的数据示例
    links = await conn.fetch('''
        SELECT * FROM "ItemLinks" LIMIT 3
    ''')
    print(f"\nItemLinks 数据示例:")
    for l in links:
        print(f"  {dict(l)}")
    
    print("\n" + "=" * 80)
    print("问题 4: 检查文件的 Path 重复情况")
    print("=" * 80)
    
    dup_files = await conn.fetch('''
        SELECT "Path", COUNT(*) as cnt
        FROM "Files"
        WHERE "Path" IS NOT NULL
        GROUP BY "Path"
        HAVING COUNT(*) > 1
        ORDER BY cnt DESC
        LIMIT 5
    ''')
    print(f"\nPath 重复的文件（前 5 个）:")
    for f in dup_files:
        print(f"  Path: {f['Path']}, 重复次数：{f['cnt']}")
        # 检查这些文件的详细信息
        file_details = await conn.fetch('''
            SELECT "Id", "Size", "Etag"
            FROM "Files"
            WHERE "Path" = $1
        ''', f['Path'])
        for fd in file_details:
            print(f"    - Id={fd['Id']}, Size={fd['Size']}, Etag={fd['Etag']}")
    
    await conn.close()

asyncio.run(check())
