"""检查视频 3102 的图片数据"""
import os
import asyncio
import asyncpg
from database.core import AsyncSessionLocal
from database.models import FileLink
from sqlalchemy import select

REMOTE_DB_CONFIG = {
    'host': os.environ.get('REMOTE_DB_HOST', ''),
    'port': int(os.environ.get('REMOTE_DB_PORT', '5432')),
    'database': os.environ.get('REMOTE_DB_NAME', ''),
    'user': os.environ.get('REMOTE_DB_USER', ''),
    'password': os.environ.get('REMOTE_DB_PASSWORD', '')
}

async def check():
    # 检查远程数据库
    print("=" * 60)
    print("远程数据库 FileImages (ItemId=3102):")
    print("=" * 60)
    remote_conn = await asyncpg.connect(**REMOTE_DB_CONFIG)
    remote_images = await remote_conn.fetch(
        'SELECT "FileId", "Type", "ImageIndex" FROM "FileImages" WHERE "ItemId" = $1 ORDER BY "ImageIndex"',
        3102
    )
    print(f"图片数量: {len(remote_images)}")
    for img in remote_images:
        print(f"  FileId={img['FileId']}, Type={img['Type']}, Index={img['ImageIndex']}")
    
    # 获取文件路径
    if remote_images:
        file_ids = [img['FileId'] for img in remote_images]
        files = await remote_conn.fetch(
            'SELECT "Id", "Path" FROM "Files" WHERE "Id" = ANY($1)',
            file_ids
        )
        print("\n文件路径:")
        for f in files:
            print(f"  {f['Id']}: {f['Path'][:80]}")
    
    await remote_conn.close()
    
    # 检查本地数据库
    print("\n" + "=" * 60)
    print("本地数据库 FileLinks (ItemId=3102):")
    print("=" * 60)
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(FileLink).where(FileLink.ItemId == 3102)
        )
        local_links = result.scalars().all()
        print(f"图片数量: {len(local_links)}")
        for link in local_links:
            print(f"  FileId={link.FileId}, Type={link.ImageType}, Index={link.ImageIndex}")

asyncio.run(check())
