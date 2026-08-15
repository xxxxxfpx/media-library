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

async def find_test_item():
    conn = await asyncpg.connect(**REMOTE_DB_CONFIG)
    # 找一个有完整伴生属性的视频
    rows = await conn.fetch('''
        SELECT mi."Id", mi."Name", mi."Type"
        FROM "MediaItems" mi
        WHERE mi."Type" = 'Movie'
        LIMIT 10
    ''')
    
    print("前10个Movie类型媒体:")
    for row in rows:
        item_id = row['Id']
        people = await conn.fetchval('SELECT COUNT(*) FROM "ItemPeople" WHERE "ItemId" = $1', item_id)
        images = await conn.fetchval('SELECT COUNT(*) FROM "FileImages" WHERE "ItemId" = $1', item_id)
        links = await conn.fetchval('SELECT COUNT(*) FROM "ItemLinks" WHERE "ItemId" = $1', item_id)
        print(f"  ID={item_id}: {row['Name'][:30]}... | 人物:{people} 图片:{images} 关联:{links}")
    
    await conn.close()

asyncio.run(find_test_item())
