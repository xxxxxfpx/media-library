"""检查远程数据库哪些 Genre 名称与 Tag 冲突"""
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

    # 获取所有 Genre 名称
    genres = await conn.fetch('SELECT "Id", "Name" FROM "MediaItems" WHERE "Type" = $1', 'Genre')
    
    # 获取所有 Tag 名称
    tags_result = await conn.fetch('SELECT "Name" FROM "MediaItems" WHERE "Type" = $1', 'Tag')
    tag_names = {r['Name'] for r in tags_result}
    
    # 获取所有已迁移的 Tag 名称（Hanime Provider 关联的）
    hanime_tags = await conn.fetch('''
        SELECT mi."Name" 
        FROM "ItemProviders" ip
        JOIN "MediaItems" mi ON ip."ItemId" = mi."Id"
        WHERE ip."ProviderId" = $1 AND mi."Type" = $2
    ''', 1, 'Tag')
    hanime_tag_names = {r['Name'] for r in hanime_tags}
    
    print("检查 Genre 名称与 Hanime Tag 冲突:")
    for g in genres:
        if g['Name'] in hanime_tag_names:
            print(f"  ⚠️  {g['Name']} (Genre Id={g['Id']}) 与 Tag 冲突")
        else:
            print(f"  ✅ {g['Name']} (Genre Id={g['Id']}) 可用")

    await conn.close()


asyncio.run(check())
