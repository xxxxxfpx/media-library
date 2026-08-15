"""查看远程数据库中 item 3102 的完整数据结构"""
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


async def main():
    conn = await asyncpg.connect(**REMOTE_DB_CONFIG)
    
    print("="*60)
    print("1. MediaItem 基本信息")
    print("="*60)
    row = await conn.fetchrow(
        '''SELECT "Id", "Type", "Name", "Overview", "PremiereDate", 
           "OfficialRating", "CommunityRating", "DateCreated"
           FROM "MediaItems" WHERE "Id" = $1''',
        3102
    )
    if row:
        for key, value in dict(row).items():
            print(f"  {key}: {value}")
    
    print("\n" + "="*60)
    print("2. FileImages 关联的图片文件")
    print("="*60)
    file_images = await conn.fetch(
        '''SELECT fi."FileId", fi."Type", fi."ImageIndex", 
           f."Name", f."Path", f."Type" as "FileType", f."Size", f."Etag"
           FROM "FileImages" fi
           JOIN "Files" f ON fi."FileId" = f."Id"
           WHERE fi."ItemId" = $1''',
        3102
    )
    for r in file_images:
        print(f"  Image: {r['Type']} (Index: {r['ImageIndex']})")
        print(f"    FileId: {r['FileId']}")
        print(f"    Path: {r['Path']}")
        print(f"    FileType: {r['FileType']}, Size: {r['Size']}")
        print()
    
    print("\n" + "="*60)
    print("3. ItemSources 视频源")
    print("="*60)
    try:
        item_sources = await conn.fetch(
            '''SELECT "FileId", "Type"
               FROM "ItemSources" WHERE "ItemId" = $1''',
            3102
        )
        for r in item_sources:
            print(f"  FileId: {r['FileId']}, Type: {r['Type']}")
            # 查询对应的文件信息
            f = await conn.fetchrow(
                '''SELECT "Path", "Type", "Size" FROM "Files" WHERE "Id" = $1''',
                r['FileId']
            )
            if f:
                print(f"    Path: {f['Path']}")
                print(f"    Type: {f['Type']}, Size: {f['Size']}")
    except Exception as e:
        print(f"  查询失败: {e}")
    
    # 获取所有关联的 FileId
    all_file_ids = set()
    for r in file_images:
        all_file_ids.add(r['FileId'])
    
    print("\n" + "="*60)
    print("4. 所有关联的 Files 详情（包含 FFmpeg 数据）")
    print("="*60)
    for file_id in all_file_ids:
        f = await conn.fetchrow(
            '''SELECT "Id", "Path", "Type", "Size", "Name", "Etag", "Data"
               FROM "Files" WHERE "Id" = $1''',
            file_id
        )
        if f:
            print(f"\n  FileId: {f['Id']}")
            print(f"  Path: {f['Path']}")
            print(f"  Type: {f['Type']}, Size: {f['Size']}")
            if f['Data']:
                try:
                    data = json.loads(f['Data'])
                    print(f"  Data: {json.dumps(data, indent=2, ensure_ascii=False)[:500]}")
                except:
                    pass
    
    # 查看是否有其他文件关联到这个 Item
    print("\n" + "="*60)
    print("5. 通过其他方式关联的 Files")
    print("="*60)
    other_files = await conn.fetch(
        '''SELECT DISTINCT f."Id", f."Path", f."Type", f."Size"
           FROM "Files" f
           JOIN "FileImages" fi ON f."Id" = fi."FileId"
           WHERE fi."ItemId" = $1''',
        3102
    )
    print(f"  通过 FileImages 关联: {len(other_files)} 个文件")
    
    await conn.close()


if __name__ == '__main__':
    asyncio.run(main())
