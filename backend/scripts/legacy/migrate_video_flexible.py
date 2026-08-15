"""
从远端数据库导入视频及其视频文件（处理ID冲突）
用法：python migrate_video_flexible.py <remote_item_id>
示例：python migrate_video_flexible.py 47
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
from sqlalchemy import select, func

REMOTE_DB_CONFIG = {
    'host': os.environ.get('REMOTE_DB_HOST', ''),
    'port': int(os.environ.get('REMOTE_DB_PORT', '5432')),
    'database': os.environ.get('REMOTE_DB_NAME', ''),
    'user': os.environ.get('REMOTE_DB_USER', ''),
    'password': os.environ.get('REMOTE_DB_PASSWORD', '')
}


async def get_new_media_item_id(local_session):
    """获取一个新的MediaItem ID"""
    result = await local_session.execute(select(func.max(MediaItem.Id)))
    max_id = result.scalar() or 0
    return max_id + 1


async def get_new_file_id(local_session):
    """获取一个新的File ID"""
    result = await local_session.execute(select(func.max(File.Id)))
    max_id = result.scalar() or 0
    return max_id + 1


async def migrate_media_item(remote_conn, local_session, remote_id):
    """迁移 MediaItem，如果ID冲突则使用新ID"""
    print(f"\n🎬 迁移 MediaItem (Remote ID={remote_id})...")
    
    row = await remote_conn.fetchrow(
        '''SELECT "Id", "Type", "Name", 
           "Overview", "Tagline", "PremiereDate", "EndDate",
           "OfficialRating", "CommunityRating", "CriticRating",
           "DateCreated", "DateModified"
           FROM "MediaItems" WHERE "Id" = $1''',
        remote_id
    )
    
    if not row:
        print(f"  ❌ 远程数据库中不存在 MediaItem {remote_id}")
        return None, None
    
    # 检查本地是否已存在相同ID
    result = await local_session.execute(select(MediaItem).where(MediaItem.Id == remote_id))
    existing = result.scalar_one_or_none()
    
    if existing:
        print(f"  ⚠️  MediaItem ID {remote_id} 已存在 ({existing.Name})，将使用新ID")
        new_id = await get_new_media_item_id(local_session)
    else:
        new_id = remote_id
    
    media_type_map = {
        'Movie': MediaType.Movie, 'Series': MediaType.Series,
        'Season': MediaType.Season, 'Episode': MediaType.Episode,
        'Audio': MediaType.Audio, 'Video': MediaType.Video,
        'Photo': MediaType.Photo, 'Book': MediaType.Book,
    }
    
    media_item = MediaItem(
        Id=new_id,
        Type=media_type_map.get(row['Type'], MediaType.Movie),
        Name=row['Name'],
        Overview=row['Overview'],
        Tagline=row['Tagline'],
        PremiereDate=row['PremiereDate'],
        EndDate=row['EndDate'],
        OfficialRating=row['OfficialRating'],
        CommunityRating=row['CommunityRating'],
        CriticRating=row['CriticRating'],
        DateCreated=row['DateCreated'] or datetime.utcnow(),
        DateModified=row['DateModified'] or datetime.utcnow(),
    )
    local_session.add(media_item)
    await local_session.commit()
    print(f"  ✅ MediaItem: {row['Name']} (ID: {new_id})")
    return new_id, remote_id


async def migrate_files_and_sources(remote_conn, local_session, new_item_id, remote_item_id):
    """迁移 Files 和 ItemSources 关联，处理File ID冲突"""
    print(f"\n📁 迁移 Files 和 Sources...")
    
    # 1. 获取 FileImages 关联的图片文件
    file_images = await remote_conn.fetch(
        '''SELECT fi."FileId", fi."Type" as "ImageType", fi."ImageIndex"
           FROM "FileImages" fi WHERE fi."ItemId" = $1''',
        remote_item_id
    )
    
    # 2. 获取 ItemSources 关联的视频文件
    item_sources = await remote_conn.fetch(
        '''SELECT isrc."FileId", isrc."Type"
           FROM "ItemSources" isrc WHERE isrc."ItemId" = $1''',
        remote_item_id
    )
    
    print(f"  发现 {len(file_images)} 个图片文件, {len(item_sources)} 个视频文件")
    
    # 迁移所有文件并记录ID映射
    id_mapping = {}  # remote_file_id -> (new_file_id, file_type, file_info)
    
    # 处理图片文件
    for r in file_images:
        remote_file_id = r['FileId']
        new_file_id, file_info = await migrate_single_file(remote_conn, local_session, remote_file_id)
        if new_file_id:
            id_mapping[remote_file_id] = ('image', new_file_id, r['ImageType'], r['ImageIndex'])
    
    # 处理视频文件
    for r in item_sources:
        remote_file_id = r['FileId']
        new_file_id, file_info = await migrate_single_file(remote_conn, local_session, remote_file_id)
        if new_file_id:
            id_mapping[remote_file_id] = ('source', new_file_id, None, None)
    
    return id_mapping


async def migrate_single_file(remote_conn, local_session, remote_file_id):
    """迁移单个文件，处理ID冲突，返回(new_file_id, file_info)"""
    # 检查本地是否已存在相同ID
    result = await local_session.execute(select(File).where(File.Id == remote_file_id))
    existing = result.scalar_one_or_none()
    
    # 从远程获取文件信息
    row = await remote_conn.fetchrow(
        '''SELECT "Id", "Etag", "Size", "Name", "SortName", 
           "Path", "CloudId", "Type", "Data"
           FROM "Files" WHERE "Id" = $1''',
        remote_file_id
    )
    
    if not row:
        print(f"  ❌ 远程不存在 File {remote_file_id}")
        return None, None
    
    remote_path = row['Path'] or ''
    
    # 如果本地已存在相同ID的文件，检查是否是同一文件
    if existing:
        if existing.Path == remote_path:
            print(f"  ⚠️  File {remote_file_id} 已存在且路径相同，跳过")
            return remote_file_id, existing
        else:
            # ID冲突，需要新ID
            new_file_id = await get_new_file_id(local_session)
            print(f"  ⚠️  File ID {remote_file_id} 冲突 ({existing.Path[:40]}...)，使用新ID {new_file_id}")
    else:
        new_file_id = remote_file_id
    
    # 提取 FFmpeg 信息
    ffmpeg_info = None
    if row['Data']:
        try:
            data = json.loads(row['Data'])
            ffmpeg_info = json.dumps(data, ensure_ascii=False)
        except:
            pass
    
    # 根据文件路径判断真实类型
    if remote_path.endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif')):
        file_type = FileType.Image
    elif remote_path.endswith(('.mp4', '.mkv', '.avi', '.mov', '.webm')):
        file_type = FileType.Video
    elif remote_path.endswith(('.mp3', '.aac', '.flac', '.wav')):
        file_type = FileType.Audio
    else:
        file_type_map = {'Video': FileType.Video, 'Audio': FileType.Audio, 'Image': FileType.Image, 'Subtitle': FileType.Subtitle}
        file_type = file_type_map.get(row['Type'], FileType.Video)
    
    file = File(
        Id=new_file_id,
        Etag=row['Etag'],
        Size=row['Size'],
        Name=row['Name'] or remote_path.split('/')[-1],
        SortName=row['SortName'],
        Path=row['Path'],
        CloudId=row['CloudId'],
        Type=file_type,
        FFmpeg=ffmpeg_info,
    )
    local_session.add(file)
    await local_session.commit()
    size_mb = (row['Size'] or 0) / (1024 * 1024)
    print(f"  ✅ File {new_file_id}: {remote_path[:50]} ({file_type.value}, {size_mb:.1f}MB)")
    return new_file_id, file


async def migrate_file_links(local_session, new_item_id, id_mapping):
    """迁移 FileLinks (图片与媒体的关联)"""
    print(f"\n🔗 迁移 FileLinks...")
    
    image_type_map = {
        'Primary': ImageType.Primary, 'Backdrop': ImageType.Backdrop,
        'Logo': ImageType.Logo, 'Thumb': ImageType.Thumb,
    }
    
    count = 0
    for remote_file_id, (source_type, new_file_id, img_type, img_index) in id_mapping.items():
        if source_type != 'image':
            continue
        
        result = await local_session.execute(
            select(FileLink).where(FileLink.ItemId == new_item_id, FileLink.FileId == new_file_id)
        )
        if result.scalar_one_or_none():
            continue
        
        link = FileLink(
            ItemId=new_item_id,
            FileId=new_file_id,
            ImageType=image_type_map.get(img_type, ImageType.Primary),
            ImageIndex=img_index or 0,
        )
        local_session.add(link)
        await local_session.commit()
        count += 1
        print(f"  ✅ FileLink: {img_type} (FileId: {new_file_id})")
    
    print(f"  总计：{count} 个图片关联")


async def migrate_file_links_for_videos(local_session, new_item_id, id_mapping):
    """迁移视频文件的 FileLink 关联"""
    print(f"\n📡 迁移视频文件的 FileLink...")
    
    count = 0
    for remote_file_id, (source_type, new_file_id, _, _) in id_mapping.items():
        if source_type != 'source':
            continue
        
        # 检查是否已存在 FileLink
        result = await local_session.execute(
            select(FileLink).where(
                FileLink.ItemId == new_item_id,
                FileLink.FileId == new_file_id
            )
        )
        if result.scalar_one_or_none():
            continue
        
        # 创建 FileLink（ImageType=None 表示不是图片）
        link = FileLink(
            ItemId=new_item_id,
            FileId=new_file_id,
            ImageType=None,  # 视频文件不需要 ImageType
            ImageIndex=0,
        )
        local_session.add(link)
        await local_session.commit()
        count += 1
        print(f"  ✅ FileLink: FileId={new_file_id} (视频)")
    
    print(f"  总计：{count} 个视频文件关联")


async def migrate_other_links(remote_conn, local_session, new_item_id, remote_item_id):
    """迁移其他关联（Genre/Studio/Tag/Person）"""
    print(f"\n🔗 迁移其他关联...")
    
    # ItemLinks
    links = await remote_conn.fetch(
        '''SELECT il."LinkedItemId", mi."Type"
           FROM "ItemLinks" il
           JOIN "MediaItems" mi ON il."LinkedItemId" = mi."Id"
           WHERE il."ItemId" = $1''',
        remote_item_id
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
                ItemLinks.ItemId == new_item_id,
                ItemLinks.LinkedItemId == r['LinkedItemId'],
                ItemLinks.Type == link_type
            )
        )
        if result.scalar_one_or_none():
            continue
        
        link = ItemLinks(
            ItemId=new_item_id,
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
            remote_item_id
        )
        people_type_map = {'Actor': PersonType.Actor, 'Director': PersonType.Director, 'Writer': PersonType.Writer, 'Producer': PersonType.Producer}
        for r in people:
            link = ItemLinks(
                ItemId=new_item_id,
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
        print("用法：python migrate_video_flexible.py <remote_item_id>")
        print("示例：python migrate_video_flexible.py 47")
        sys.exit(1)
    
    remote_item_id = int(sys.argv[1])
    
    print("="*60)
    print(f"迁移视频（含视频文件）Remote ID={remote_item_id}")
    print("="*60)
    
    print("\n🔗 连接远程 PostgreSQL...")
    remote_conn = await asyncpg.connect(**REMOTE_DB_CONFIG)
    print("✅ 连接成功")
    
    async with AsyncSessionLocal() as local_session:
        # 1. 迁移 MediaItem（处理ID冲突）
        new_item_id, remote_id = await migrate_media_item(remote_conn, local_session, remote_item_id)
        if not new_item_id:
            await remote_conn.close()
            return
        
        # 2. 迁移 Files（包括视频文件和图片，处理File ID冲突）
        id_mapping = await migrate_files_and_sources(remote_conn, local_session, new_item_id, remote_item_id)
        
        # 3. 迁移 FileLinks（图片关联）
        await migrate_file_links(local_session, new_item_id, id_mapping)
        
        # 4. 迁移视频文件的 FileLink
        await migrate_file_links_for_videos(local_session, new_item_id, id_mapping)
        
        # 5. 迁移其他关联
        await migrate_other_links(remote_conn, local_session, new_item_id, remote_item_id)
    
    await remote_conn.close()
    
    print("\n" + "="*60)
    print("✅ 迁移完成！")
    print(f"访问：http://localhost:5173/media/{new_item_id}")
    print("="*60)


if __name__ == '__main__':
    asyncio.run(main())
