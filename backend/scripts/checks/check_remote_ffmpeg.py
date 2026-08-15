"""检查远程数据库 Files.Data 字段（FFmpeg数据）"""
import os
import asyncio
import asyncpg
import json

REMOTE_DB_CONFIG = {
    'host': os.environ.get('REMOTE_DB_HOST', ''),
    'port': int(os.environ.get('REMOTE_DB_PORT', '5432')),
    'database': os.environ.get('REMOTE_DB_NAME', ''),
    'user': os.environ.get('REMOTE_DB_USER', ''),
    'password': os.environ.get('REMOTE_DB_PASSWORD', '')
}

async def check_remote_ffmpeg():
    print("=" * 60)
    print("检查远程数据库 Files.Data 字段")
    print("=" * 60)

    conn = await asyncpg.connect(**REMOTE_DB_CONFIG)

    # 总文件数
    total = await conn.fetchval('SELECT COUNT(*) FROM "Files"')
    print(f"\n远程 Files 总数: {total}")

    # Video 类型文件数
    video_count = await conn.fetchval('''
        SELECT COUNT(*) FROM "Files" WHERE "Type" = 'Video'
    ''')
    print(f"Video 类型文件数: {video_count}")

    # 显示几个有 Data 的示例
    print("\n查询有 Data 的文件示例:")
    rows = await conn.fetch('''
        SELECT "Id", "Name", "Type", "Data"
        FROM "Files"
        WHERE "Data" IS NOT NULL
        LIMIT 5
    ''')

    has_data_count = 0
    for row in rows:
        data_str = str(row['Data'])[:100] if row['Data'] else 'None'
        print(f"  ID={row['Id']}, Type={row['Type']}, Data={data_str}...")
        if row['Data']:
            has_data_count += 1

    print(f"\n前5条中有Data的: {has_data_count}")

    await conn.close()
    print("\n✅ 检查完成")

asyncio.run(check_remote_ffmpeg())