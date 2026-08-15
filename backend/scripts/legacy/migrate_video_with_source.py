"""
从远端数据库导入视频及其视频文件（包括 ItemSources 关联）
用法：python migrate_video_with_source.py <item_id>
示例：python migrate_video_with_source.py 4
"""
import os
import asyncio
import asyncpg
import json
import sys
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
    
    result = await local_session.execute(
        select(MediaItem).where(MediaItem.Id == item_id)
    )
    if result.scalar_one_or_none():
        print(f"  ⚠️  MediaItem {item_id} 已存在，跳过")
        return True
    
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


async def migrate_files_and_sources(remote_conn, local_session, item_id):
    """迁移 Files 和 ItemSources 关联"""
    print(f"\n📁 迁移 Files 和 Sources (ItemId={item_id})...")
    
    # 1. 获取 FileImages 关联的图片文件
    file_images = await remote_conn.fetch(
        '''SELECT fi."FileId", fi."Type" as "ImageType", fi."ImageIndex"
           FROM "FileImages" fi WHERE fi."ItemId" = $1''',
        item_id
    )
    
    # 2. 获取 ItemSources 关联的视频文件
    item_sources = await remote_conn.fetch(
        '''SELECT isrc."FileId", isrc."Type"
           FROM "ItemSources" isrc WHERE isrc."ItemId" = $1''',
        item_id
    )
    
    all_file_ids = set()
    for r in file_images:
        all_file_ids.add((r['FileId'], 'image'))
    for r in item_sources:
        all_file_ids.add((r['FileId'], 'source'))
    
    print(f"  发现 {len(all_file_ids)} 个关联文件 ({len(file_images)} 图片 + {len(item_sources)} 视频)")
    
    migrated_count = 0
    for file_id, source_type in all_file_ids:
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
        size_mb = (row['Size'] or 0) / (1024 * 1024)
        print(f"  ✅ File {file_id}: {file_path[:50]} ({file_type.value}, {size_mb:.1f}MB)")
    
    print(f"  总计：{migrated_count} 个文件迁移成功")
    return all_file_ids


async def migrate_file_links(remote_conn, local_session, item_id):
    """迁移 FileLinks (图片与媒体的关联)"""
    print(f"\n🔗 迁移 FileLinks (ItemId={item_id})...")
    
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
        result = await local_session.execute(
            select(FileLink).where(
                FileLink.ItemId == item_id,
                FileLink.FileId == r['FileId']
            )
        )
        if result.scalar_one_or_none():
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
    
    print(f"  总计：{migrated_count} 个 FileLink")


async def migrate_item_sources_links(remote_conn, local_session, item_id):
    """迁移 ItemSources 关联（视频文件关联）"""
    print(f"\n📡 迁移 ItemSources 关联 (ItemId={item_id})...")
    
    item_sources = await remote_conn.fetch(
        '''SELECT "FileId", "Type"
           FROM "ItemSources" WHERE "ItemId" = $1''',
        item_id
    )
    
    migrated_count = 0
    for r in item_sources:
        # 将 ItemSources 作为 Source 类型的 ItemLinks
        result = await local_session.execute(
            select(ItemLinks).where(
                ItemLinks.ItemId == item_id,
                ItemLinks.LinkedItemId == r['FileId'],
                ItemLinks.Type == ItemLinkType.Source
            )
        )
        if result.scalar_one_or_none():
            continue
        
        link = ItemLinks(
            ItemId=item_id,
            LinkedItemId=r['FileId'],
            Type=ItemLinkType.Source,
        )
        local_session.add(link)
        await local_session.commit()
        migrated_count += 1
        print(f"  ✅ Source: FileId={r['FileId']}")
    
    print(f"  总计：{migrated_count} 个视频源关联")


async def migrate_other_links(remote_conn, local_session, item_id):
    """迁移其他关联（Genre/Studio/Tag/Person）"""
    print(f"\n🔗 迁移其他关联 (ItemId={item_id})...")
    
    # ItemLinks
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
        'Source': ItemLinkType.Source, 'BoxSet': ItemLinkType.Source,
    }
    
    for r in links:
        link_type = type_map.get(r['Type'], ItemLinkType.Source)
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
    
    # ItemPeople
    try:
        people = await remote_conn.fetch(
            '''SELECT "PersonId", "Role", "Type" 
               FROM "ItemPeople" WHERE "ItemId" = $1''',
            item_id
        )
        people_type_map = {
            'Actor': PersonType.Actor, 'Director': PersonType.Director,
            'Writer': PersonType.Writer, 'Producer': PersonType.Producer,
        }
        for r in people:
            link = ItemLinks(
                ItemId=item_id,
                LinkedItemId=r['PersonId'],
                Type=ItemLinkType.Person,
                PeopleType=people_type_map.get(r['Type'], PersonType.Actor),
                PeopleRole=r['Role'],
            )
            local_session.add(link)
            await local_session.commit()
        print(f"  ✅ {len(people)} 个人物关联")
    except:
        pass
    
    print(f"  ✅ {len(links)} 个其他关联")


async def main():
    if len(sys.argv) < 2:
        print("用法：python migrate_video_with_source.py <item_id>")
        print("示例：python migrate_video_with_source.py 4")
        sys.exit(1)
    
    item_id = int(sys.argv[1])
    
    print("="*60)
    print(f"迁移视频（含视频文件）ID={item_id}")
    print("="*60)
    
    print("\n🔗 连接远程 PostgreSQL...")
    remote_conn = await asyncpg.connect(**REMOTE_DB_CONFIG)
    print("✅ 连接成功")
    
    async with AsyncSessionLocal() as local_session:
        # 1. 迁移 MediaItem
        success = await migrate_media_item(remote_conn, local_session, item_id)
        if not success:
            await remote_conn.close()
            return
        
        # 2. 迁移 Files（包括视频文件和图片）
        await migrate_files_and_sources(remote_conn, local_session, item_id)
        
        # 3. 迁移 FileLinks（图片关联）
        await migrate_file_links(remote_conn, local_session, item_id)
        
        # 4. 迁移 ItemSources 关联（视频文件关联）
        await migrate_item_sources_links(remote_conn, local_session, item_id)
        
        # 5. 迁移其他关联
        await migrate_other_links(remote_conn, local_session, item_id)
    
    await remote_conn.close()
    
    print("\n" + "="*60)
    print("✅ 迁移完成！")
    print(f"访问：http://localhost:5173/media/{item_id}")
    print("="*60)


if __name__ == '__main__':
    asyncio.run(main())
