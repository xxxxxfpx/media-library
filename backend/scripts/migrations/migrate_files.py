"""迁移 Hanime 关联的文件信息"""
import os
import asyncio
import asyncpg
from datetime import datetime, timezone, timedelta
from database.core import AsyncSessionLocal
from database.models import File, FileLink
from database.models.enums import ImageType
from sqlalchemy import select


async def migrate_files():
    conn = await asyncpg.connect(
        host=os.environ.get('REMOTE_DB_HOST', ''),
        port=int(os.environ.get('REMOTE_DB_PORT', '5432')),
        database=os.environ.get('REMOTE_DB_NAME', ''),
        user=os.environ.get('REMOTE_DB_USER', ''),
        password=os.environ.get('REMOTE_DB_PASSWORD', '')
    )
    
    async with AsyncSessionLocal() as s:
        # 1. 迁移 Files（以 Path 去重）
        print("\n=== 迁移 Files ===")
        
        # 获取所有 Hanime 关联的文件
        hanime_file_ids = await conn.fetch('''
            SELECT DISTINCT f."Id"
            FROM "Files" f
            LEFT JOIN "FileImages" fi ON f."Id" = fi."FileId"
            LEFT JOIN "ItemSources" isrc ON f."Id" = isrc."FileId"
            LEFT JOIN "ItemProviders" ip1 ON fi."ItemId" = ip1."ItemId"
            LEFT JOIN "ItemProviders" ip2 ON isrc."ItemId" = ip2."ItemId"
            WHERE ip1."ProviderId" = 1 OR ip2."ProviderId" = 1
        ''')
        hanime_file_id_list = [r['Id'] for r in hanime_file_ids]
        print(f'需要迁移的文件数: {len(hanime_file_id_list)}')
        
        # 获取本地已有 Path
        existing_paths = await s.execute(select(File.Path))
        existing_path_set = {row[0] for row in existing_paths.all() if row[0]}
        
        created = 0
        skipped = 0
        
        for file_id in hanime_file_id_list:
            file_data = await conn.fetchrow('SELECT * FROM "Files" WHERE "Id" = $1', file_id)
            
            if file_data['Path'] in existing_path_set:
                skipped += 1
                continue
            
            file = File(
                Id=file_data['Id'],
                Etag=file_data['Etag'],
                Size=file_data['Size'],
                Name=file_data['Name'],
                SortName=file_data['SortName'],
                Path=file_data['Path'],
                CloudId=file_data['CloudId'],
                Type=file_data['Type'],
            )
            s.add(file)
            existing_path_set.add(file_data['Path'])
            created += 1
            
            if created % 1000 == 0:
                await s.commit()
                print(f'  已插入 {created} 个，跳过 {skipped} 个')
        
        await s.commit()
        print(f'✅ 创建 {created} 个文件，跳过 {skipped} 个已存在')
        
        # 2. 迁移 FileLinks（图片）
        print("\n=== 迁移 FileLinks（图片）===")
        image_links = await conn.fetch('''
            SELECT fi."ItemId", fi."FileId", fi."Type", fi."ImageIndex"
            FROM "FileImages" fi
            JOIN "ItemProviders" ip ON fi."ItemId" = ip."ItemId"
            WHERE ip."ProviderId" = 1
        ''')
        print(f'远程图片关联: {len(image_links)} 个')
        
        # 获取本地已有
        existing_links = await s.execute(select(FileLink.ItemId, FileLink.FileId, FileLink.ImageType))
        existing_link_set = set()
        for row in existing_links.all():
            existing_link_set.add((row.ItemId, row.FileId, str(row.ImageType) if row.ImageType else None))
        
        # 映射远程 Type 到本地 ImageType
        image_type_map = {
            'Primary': ImageType.Primary,
            'Backdrop': ImageType.Backdrop,
            'Logo': ImageType.Logo,
            'Thumb': ImageType.Thumb,
        }
        
        created = 0
        for link in image_links:
            local_image_type = image_type_map.get(link['Type'])
            key = (link['ItemId'], link['FileId'], str(local_image_type) if local_image_type else None)
            
            if key in existing_link_set:
                continue
            
            file_link = FileLink(
                ItemId=link['ItemId'],
                FileId=link['FileId'],
                ImageType=local_image_type,
                ImageIndex=link['ImageIndex'] or 0,
            )
            s.add(file_link)
            created += 1
            if created % 500 == 0:
                await s.commit()
                print(f'  已插入 {created} 个')
        
        await s.commit()
        print(f'✅ 创建 {created} 个图片关联')
        
        # 3. 迁移 FileLinks（视频）
        print("\n=== 迁移 FileLinks（视频）===")
        video_links = await conn.fetch('''
            SELECT isrc."ItemId", isrc."FileId"
            FROM "ItemSources" isrc
            JOIN "ItemProviders" ip ON isrc."ItemId" = ip."ItemId"
            WHERE ip."ProviderId" = 1
        ''')
        print(f'远程视频关联: {len(video_links)} 个')
        
        created = 0
        for link in video_links:
            key = (link['ItemId'], link['FileId'], None)
            
            if key in existing_link_set:
                continue
            
            file_link = FileLink(
                ItemId=link['ItemId'],
                FileId=link['FileId'],
                ImageType=None,
                ImageIndex=0,
            )
            s.add(file_link)
            created += 1
            if created % 500 == 0:
                await s.commit()
                print(f'  已插入 {created} 个')
        
        await s.commit()
        print(f'✅ 创建 {created} 个视频关联')
    
    await conn.close()
    print("\n✅ 文件迁移完成！")


asyncio.run(migrate_files())
