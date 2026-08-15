"""
检查远程数据库中的伴生属性表结构
"""
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

async def check_table_structure(conn, table_name):
    """检查表结构"""
    print(f"\n📋 表: {table_name}")
    print("-" * 60)
    
    # 获取列信息
    rows = await conn.fetch(
        '''SELECT column_name, data_type, is_nullable
           FROM information_schema.columns
           WHERE table_schema = 'public' AND table_name = $1
           ORDER BY ordinal_position''',
        table_name
    )
    
    for row in rows:
        print(f"  {row['column_name']:30} {row['data_type']:20} {row['is_nullable']}")
    
    # 获取记录数
    count = await conn.fetchval(f'SELECT COUNT(*) FROM "{table_name}"')
    print(f"\n  记录数: {count}")
    
    # 获取样例数据
    sample = await conn.fetch(f'SELECT * FROM "{table_name}" LIMIT 3')
    if sample:
        print(f"\n  样例数据:")
        for row in sample:
            print(f"    {dict(row)}")

async def main():
    conn = await asyncpg.connect(**REMOTE_DB_CONFIG)
    
    # 检查伴生属性相关表
    association_tables = [
        'ItemLinks',      # 通用关联
        'ItemPeople',     # 人物关联
        'ItemSources',    # 来源关联
        'ItemProviders',  # 提供者关联
        'FileImages',     # 文件图片
        'Providers',      # 提供者列表
    ]
    
    print("=" * 60)
    print("远程数据库伴生属性表结构")
    print("=" * 60)
    
    for table in association_tables:
        try:
            await check_table_structure(conn, table)
        except Exception as e:
            print(f"\n❌ 表 {table} 不存在或无法访问: {e}")
    
    await conn.close()

if __name__ == '__main__':
    asyncio.run(main())
