"""检查远程数据库枚举值"""
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
    
    # 查询枚举值
    enum_values = await conn.fetch("""
        SELECT unnest(enum_range(NULL::media_type_enum))::text as value
    """)
    print('远程 media_type_enum 枚举值:')
    for row in enum_values:
        print(f"  '{row['value']}'")
    
    # 验证不同的写法
    test_values = ['source', 'Source', 'SOURCE', 'movie', 'Movie']
    for v in test_values:
        try:
            count = await conn.fetchval(
                "SELECT COUNT(*) FROM \"MediaItems\" WHERE \"Type\" = $1::media_type_enum",
                v
            )
            print(f"\n测试 '{v}': {count} 条记录")
        except Exception as e:
            print(f"\n测试 '{v}': 错误 - {e}")
    
    await conn.close()


asyncio.run(check())
