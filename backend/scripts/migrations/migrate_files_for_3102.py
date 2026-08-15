"""迁移视频 3102 的 Files 记录"""
import os
import asyncio
import asyncpg
import json
from database.core import AsyncSessionLocal
from database.models import File, FileType
from sqlalchemy import select

REMOTE_DB_CONFIG = {
    'host': os.environ.get('REMOTE_DB_HOST', ''),
    'port': int(os.environ.get('REMOTE_DB_PORT', '5432')),
    'database': os.environ.get('REMOTE_DB_NAME', ''),
    'user': os.environ.get('REMOTE_DB_USER', ''),
    'password': os.environ.get('REMOTE_DB_PASSWORD', '')
}


async def migrate_files():
    remote_conn = await asyncpg.connect(**REMOTE_DB_CONFIG)
    
    async with AsyncSessionLocal() as session:
        # 获取 FileLinks 关联的 FileId
        from database.models import FileLink
        result = await session.execute(
            select(FileLink.FileId).where(FileLink.ItemId == 3102)
        )
        file_ids = [r[0] for r in result.all()]
        print(f"FileLinks 中的 FileIds: {file_ids}")
        
        # 从远程获取这些文件
        for file_id in file_ids:
            # 检查本地是否已存在
            result = await session.execute(
                select(File).where(File.Id == file_id)
            )
            if result.scalar_one_or_none():
                print(f"  File {file_id} 已存在，跳过")
                continue
            
            # 从远程获取
            row = await remote_conn.fetchrow(
                '''SELECT "Id", "Etag", "Size", "Name", "SortName", 
                   "Path", "CloudId", "Type", "Data"
                   FROM "Files" WHERE "Id" = $1''',
                file_id
            )
            
            if not row:
                print(f"  ❌ 远程不存在 File {file_id}")
                continue
            
            # 提取 FFmpeg 信息
            ffmpeg_info = None
            if row['Data']:
                try:
                    data = json.loads(row['Data'])
                    ffmpeg_info = json.dumps(data, ensure_ascii=False)
                except:
                    pass
            
            # 确定 FileType
            file_type_map = {
                'Video': FileType.Video,
                'Audio': FileType.Audio,
                'Image': FileType.Image,
                'Subtitle': FileType.Subtitle,
            }
            file_type = file_type_map.get(row['Type'], FileType.Video)
            
            # 创建本地 File 记录
            file = File(
                Id=row['Id'],
                Etag=row['Etag'],
                Size=row['Size'],
                Name=row['Name'] or f"file_{file_id}",
                SortName=row['SortName'],
                Path=row['Path'],
                CloudId=row['CloudId'],
                Type=file_type,
                FFmpeg=ffmpeg_info,
            )
            session.add(file)
            print(f"  ✅ 添加 File {file_id}: {row['Path'][:50]}")
        
        await session.commit()
    
    await remote_conn.close()
    print("\n✅ Files 迁移完成！")


if __name__ == '__main__':
    asyncio.run(migrate_files())
