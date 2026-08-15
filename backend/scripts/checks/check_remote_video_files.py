"""查看远程数据库中有视频文件关联的媒体"""
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


async def main():
    conn = await asyncpg.connect(**REMOTE_DB_CONFIG)
    
    print("="*60)
    print("查找有视频文件关联的媒体")
    print("="*60)
    
    # 查找通过 ItemSources 关联到视频文件的媒体
    rows = await conn.fetch('''
        SELECT DISTINCT mi."Id", mi."Name", mi."Type", f."Id" as "FileId", f."Path", f."Type" as "FileType", f."Size"
        FROM "MediaItems" mi
        JOIN "ItemSources" isrc ON mi."Id" = isrc."ItemId"
        JOIN "Files" f ON isrc."FileId" = f."Id"
        WHERE f."Path" LIKE '%.mp4' OR f."Path" LIKE '%.mkv' OR f."Path" LIKE '%.avi'
        ORDER BY mi."Id"
        LIMIT 10
    ''')
    
    print(f"\n找到 {len(rows)} 个有视频文件的媒体:\n")
    for r in rows:
        print(f"MediaID: {r['Id']}, Name: {r['Name']}")
        print(f"  FileID: {r['FileId']}, Path: {r['Path']}")
        print(f"  FileType: {r['FileType']}, Size: {r['Size']}")
        print()
    
    await conn.close()


if __name__ == '__main__':
    asyncio.run(main())
