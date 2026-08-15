"""
完整迁移视频 3102 及其所有关联数据
- MediaItem (影片信息)
- Files (文件记录，包括图片和视频)
- FileLinks (文件与媒体的关联)
- ItemLinks (其他关联如 Genre/Studio/Tag/Person)
"""
import os
import asyncio
import asyncpg
import json
from datetime import datetime
from database.core import AsyncSessionLocal
from database.models import (
    MediaItem, MediaType, File, FileType,
    FileLink, ImageType, ItemLinks, ItemLinkType, PersonType
)
from sqlalchemy import select

REMOTE_DB_CONFIG = {
    'host': os.environ.get('REMOTE_DB_HOST', ''),
    'port': int(os.environ.get('REMOTE_DB_PORT', '5432')),
    'database': os.environ.get('REMOTE_DB_NAME', ''),
    'user': os.environ.get('REMOTE_DB_USER', ''),
    'password': os.environ.get('REMOTE_DB_PASSWORD', '')
}


async def migrate_media_item(remote_conn, local_session, item_id):
    """迁移 MediaItem"""
    print(f"\n🎬 迁移 MediaItem (ID={item_id})...")
    
    # 检查本地是否已存在
    result = await local_session.execute(
        select(MediaItem).where(MediaItem.Id == item_id)
    )
    if result.scalar_one_or_none():
        print(f"  ⚠️  MediaItem {item_id} 已存在，跳过")
        return True
    
    # 从远程获取
    row = await remote_conn.fetchrow(
        '''SELECT "Id", "Type", "Name", "OriginalTitle", "SortName", 
           "Overview", "Tagline", "PremiereDate", "EndDate",
           "OfficialRating", "CommunityRating", "CriticRating",
           "DateCreated", "DateModified", "IsDeleted"
           FROM "MediaItems" WHERE "Id" = $1''',
        item_id
    )
    
    if not row:
        print(f"  ❌ 远程数据库中不存在 MediaItem {item_id}")
        return False
    
    media_type_map = {
        'Movie': MediaType.Movie, 'Series': MediaType.Series,
        'Season': MediaType.Season, 'Episode': MediaType.Episode,
        'Audio': MediaType.Audio, 'Video': MediaType.Video,
        'Photo': MediaType.Photo, 'Book': MediaType.Book,
    }
    
    media_item = MediaItem(
        Id=row['Id'],
        Type=media_type_map.get(row['Type'], MediaType.Movie),
        Name=row['Name'],
        OriginalTitle=row['OriginalTitle'],
        SortName=row['SortName'],
        Overview=row['Overview'],
        Tagline=row['Tagline'],
        PremiereDate=row['PremiereDate'],
        EndDate=row['EndDate'],
        OfficialRating=row['OfficialRating'],
        CommunityRating=row['CommunityRating'],
        CriticRating=row['CriticRating'],
        DateCreated=row['DateCreated'] or datetime.utcnow(),
        DateModified=row['DateModified'] or datetime.utcnow(),
        IsDeleted=row['IsDeleted'] or False,
    )
    local_session.add(media_item)
    await local_session.commit()
    print(f"  ✅ MediaItem: {row['Name']}")
    return True


async def migrate_files(remote_conn, local_session, item_id):
    """迁移与 item 关联的所有 Files"""
    print(f"\n📁 迁移 Files (ItemId={item_id})...")
    
    # 获取 FileImages 关联的文件
    file_images = await remote_conn.fetch(
        '''SELECT fi."FileId", fi."Type" as "ImageType", fi."ImageIndex"
           FROM "FileImages" fi WHERE fi."ItemId" = $1''',
        item_id
    )
    
    # 获取 ItemSources 关联的文件
    try:
        item_sources = await remote_conn.fetch(
            '''SELECT "FileId", "Type" FROM "ItemSources" WHERE "ItemId" = $1''',
            item_id
        )
    except:
        item_sources = []
    
    # 收集所有 FileId
    all_file_ids = set()
    for r in file_images:
        all_file_ids.add(r['FileId'])
    for r in item_sources:
        all_file_ids.add(r['FileId'])
    
    print(f"  发现 {len(all_file_ids)} 个关联文件")
    
    migrated_count = 0
    for file_id in all_file_ids:
        # 检查本地是否已存在
        result = await local_session.execute(
            select(File).where(File.Id == file_id)
        )
        if result.scalar_one_or_none():
            print(f"  ⚠️  File {file_id} 已存在，跳过")
            continue
        
        # 从远程获取文件信息
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
        
        # 根据文件路径判断真实类型
        file_path = row['Path'] or ''
        if file_path.endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif')):
            file_type = FileType.Image
        elif file_path.endswith(('.mp4', '.mkv', '.avi', '.mov', '.webm')):
            file_type = FileType.Video
        elif file_path.endswith(('.mp3', '.aac', '.flac', '.wav')):
            file_type = FileType.Audio
        else:
            # 回退到数据库中的类型
            file_type_map = {
                'Video': FileType.Video, 'Audio': FileType.Audio,
                'Image': FileType.Image, 'Subtitle': FileType.Subtitle,
            }
            file_type = file_type_map.get(row['Type'], FileType.Video)
        
        file = File(
            Id=row['Id'],
            Etag=row['Etag'],
            Size=row['Size'],
            Name=row['Name'] or file_path.split('/')[-1],
            SortName=row['SortName'],
            Path=row['Path'],
            CloudId=row['CloudId'],
            Type=file_type,
            FFmpeg=ffmpeg_info,
        )
        local_session.add(file)
        await local_session.commit()
        migrated_count += 1
        print(f"  ✅ File {file_id}: {file_path[:60]} ({file_type.value})")
    
    print(f"  总计: {migrated_count} 个文件迁移成功")
    return all_file_ids


async def migrate_file_links(remote_conn, local_session, item_id):
    """迁移 FileLinks (文件与媒体的关联)"""
    print(f"\n🔗 迁移 FileLinks (ItemId={item_id})...")
    
    # 获取 FileImages
    file_images = await remote_conn.fetch(
        '''SELECT "FileId", "Type", "ImageIndex" 
           FROM "FileImages" WHERE "ItemId" = $1''',
        item_id
    )
    
    image_type_map = {
        'Primary': ImageType.Primary, 'Backdrop': ImageType.Backdrop,
        'Logo': ImageType.Logo, 'Thumb': ImageType.Thumb,
    }
    
    migrated_count = 0
    for r in file_images:
        # 检查本地是否已存在
        result = await local_session.execute(
            select(FileLink).where(
                FileLink.ItemId == item_id,
                FileLink.FileId == r['FileId']
            )
        )
        if result.scalar_one_or_none():
            print(f"  ⚠️  FileLink (Item={item_id}, File={r['FileId']}) 已存在")
            continue
        
        link = FileLink(
            ItemId=item_id,
            FileId=r['FileId'],
            ImageType=image_type_map.get(r['Type'], ImageType.Primary),
            ImageIndex=r['ImageIndex'] or 0,
        )
        local_session.add(link)
        await local_session.commit()
        migrated_count += 1
        print(f"  ✅ FileLink: {r['Type']} (Index: {r['ImageIndex']})")
    
    print(f"  总计: {migrated_count} 个 FileLink 迁移成功")


async def migrate_item_links(remote_conn, local_session, item_id):
    """迁移 ItemLinks (Genre/Studio/Tag/Person 关联)"""
    print(f"\n🔗 迁移 ItemLinks (ItemId={item_id})...")
    
    # 获取所有关联项
    links = await remote_conn.fetch(
        '''SELECT il."LinkedItemId", mi."Type"
           FROM "ItemLinks" il
           JOIN "MediaItems" mi ON il."LinkedItemId" = mi."Id"
           WHERE il."ItemId" = $1''',
        item_id
    )
    
    type_map = {
        'Genre': ItemLinkType.Genre, 'Studio': ItemLinkType.Studio,
        'Tag': ItemLinkType.Tag, 'Person': ItemLinkType.Person,
        'Source': ItemLinkType.Source,
    }
    
    migrated_count = 0
    for r in links:
        link_type = type_map.get(r['Type'], ItemLinkType.Source)
        
        # 检查本地是否已存在
        result = await local_session.execute(
            select(ItemLinks).where(
                ItemLinks.ItemId == item_id,
                ItemLinks.LinkedItemId == r['LinkedItemId'],
                ItemLinks.Type == link_type
            )
        )
        if result.scalar_one_or_none():
            continue
        
        link = ItemLinks(
            ItemId=item_id,
            LinkedItemId=r['LinkedItemId'],
            Type=link_type,
        )
        local_session.add(link)
        await local_session.commit()
        migrated_count += 1
        print(f"  ✅ ItemLink: {r['Type']} -> {r['LinkedItemId']}")
    
    print(f"  总计: {migrated_count} 个 ItemLink 迁移成功")


async def migrate_item_people(remote_conn, local_session, item_id):
    """迁移 ItemPeople (人物关联)"""
    print(f"\n👥 迁移 ItemPeople (ItemId={item_id})...")
    
    try:
        people = await remote_conn.fetch(
            '''SELECT "PersonId", "Role", "Type" 
               FROM "ItemPeople" WHERE "ItemId" = $1''',
            item_id
        )
    except:
        print("  ⚠️  ItemPeople 表不存在或查询失败")
        return
    
    people_type_map = {
        'Actor': PersonType.Actor, 'Director': PersonType.Director,
        'Writer': PersonType.Writer, 'Producer': PersonType.Producer,
    }
    
    migrated_count = 0
    for r in people:
        # 检查本地是否已存在
        result = await local_session.execute(
            select(ItemLinks).where(
                ItemLinks.ItemId == item_id,
                ItemLinks.LinkedItemId == r['PersonId'],
                ItemLinks.Type == ItemLinkType.Person
            )
        )
        if result.scalar_one_or_none():
            continue
        
        link = ItemLinks(
            ItemId=item_id,
            LinkedItemId=r['PersonId'],
            Type=ItemLinkType.Person,
            PeopleType=people_type_map.get(r['Type'], PersonType.Actor),
            PeopleRole=r['Role'],
        )
        local_session.add(link)
        await local_session.commit()
        migrated_count += 1
        print(f"  ✅ Person: {r['Type']} - {r['Role']}")
    
    print(f"  总计: {migrated_count} 个人物关联迁移成功")


async def main():
    item_id = 3102
    
    print("="*60)
    print(f"完整迁移视频 ID={item_id}")
    print("="*60)
    
    # 连接远程数据库
    print("\n🔗 连接远程 PostgreSQL...")
    remote_conn = await asyncpg.connect(**REMOTE_DB_CONFIG)
    print("✅ 连接成功")
    
    async with AsyncSessionLocal() as local_session:
        # 1. 迁移 MediaItem
        success = await migrate_media_item(remote_conn, local_session, item_id)
        if not success:
            await remote_conn.close()
            return
        
        # 2. 迁移 Files
        file_ids = await migrate_files(remote_conn, local_session, item_id)
        
        # 3. 迁移 FileLinks
        await migrate_file_links(remote_conn, local_session, item_id)
        
        # 4. 迁移 ItemLinks (Genre/Studio/Tag)
        await migrate_item_links(remote_conn, local_session, item_id)
        
        # 5. 迁移 ItemPeople
        await migrate_item_people(remote_conn, local_session, item_id)
    
    await remote_conn.close()
    
    print("\n" + "="*60)
    print("✅ 完整迁移完成！")
    print("="*60)


if __name__ == '__main__':
    asyncio.run(main())
