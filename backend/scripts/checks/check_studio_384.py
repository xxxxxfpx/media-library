"""检查 Studio 384 的图片数据"""
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

async def check():
    conn = await asyncpg.connect(**REMOTE_DB_CONFIG)
    
    print("=" * 60)
    print("远程数据库中 ItemId=384 的文件图片:")
    print("=" * 60)
    
    # 检查 FileImages
    images = await conn.fetch(
        'SELECT "FileId", "Type", "ImageIndex" FROM "FileImages" WHERE "ItemId" = $1',
        384
    )
    print(f"FileImages: {len(images)} 条")
    for img in images:
        print(f"  FileId={img['FileId']}, Type={img['Type']}")
        # 获取文件路径
        file = await conn.fetchrow(
            'SELECT "Path" FROM "Files" WHERE "Id" = $1',
            img['FileId']
        )
        if file:
            print(f"    Path: {file['Path']}")
    
    # 检查 ItemLinks 中的关联（Studio 可能有 logo 图片）
    print("\n" + "=" * 60)
    print("远程数据库中 ItemId=384 的 ItemLinks:")
    print("=" * 60)
    links = await conn.fetch(
        'SELECT "LinkedItemId" FROM "ItemLinks" WHERE "ItemId" = $1',
        384
    )
    print(f"ItemLinks: {len(links)} 条")
    
    await conn.close()

asyncio.run(check())
