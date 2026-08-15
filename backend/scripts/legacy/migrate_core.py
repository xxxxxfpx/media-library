"""
核心数据迁移脚本
- MediaItems (影片/媒体)
- Files (文件)
- ItemLinks (关联关系)
- ItemPeople (人物关联 → ItemLinks)
- FileImages (文件图片 → FileLinks)
- ItemSources (来源关联 → ItemLinks)
- Providers (来源 → Source类型 MediaItems)

不迁移:
- Users, UserData (用户数据)
- 媒体库类型相关数据
"""
import os
import asyncio
import asyncpg
import json
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from database.core import AsyncSessionLocal, engine
from database.models import (
    MediaItem, MediaType, File, FileType,
    ItemLinks, LinkType, FileLink, ImageType,
    PeopleType
)
from sqlalchemy import select, text
from tqdm import tqdm

# 远程数据库配置
REMOTE_DB_CONFIG = {
    'host': os.environ.get('REMOTE_DB_HOST', ''),
    'port': int(os.environ.get('REMOTE_DB_PORT', '5432')),
    'database': os.environ.get('REMOTE_DB_NAME', ''),
    'user': os.environ.get('REMOTE_DB_USER', ''),
    'password': os.environ.get('REMOTE_DB_PASSWORD', '')
}

# 类型映射
MEDIA_TYPE_MAP = {
    'Movie': MediaType.Movie,
    'Series': MediaType.Series,
    'Season': MediaType.Season,
    'Episode': MediaType.Episode,
    'Audio': MediaType.Audio,
    'Video': MediaType.Video,
    'Photo': MediaType.Photo,
    'Book': MediaType.Book,
    'Person': MediaType.Person,
    'Genre': MediaType.Genre,
    'Studio': MediaType.Studio,
    'Tag': MediaType.Tag,
    'Source': MediaType.Source,
}

FILE_TYPE_MAP = {
    'Video': FileType.Video,
    'Audio': FileType.Audio,
    'Image': FileType.Image,
    'Subtitle': FileType.Subtitle,
}


class MigrationStats:
    def __init__(self):
        self.stats = {}
    
    def record(self, table, count):
        self.stats[table] = count
        print(f"  ✅ {table}: {count} 条记录")
    
    def show_summary(self):
        print("\n" + "="*60)
        print("迁移完成统计")
        print("="*60)
        for table, count in self.stats.items():
            print(f"  {table:20s}: {count:6d}")


stats = MigrationStats()


async def migrate_providers(remote_conn, local_session):
    """迁移 Providers 为 Source 类型的 MediaItems"""
    print("\n📦 迁移 Providers → Source...")
    
    rows = await remote_conn.fetch('SELECT "Id", "Name", "Url", "Description" FROM "Providers"')
    
    id_mapping = {}  # 旧ID -> 新ID
    
    for row in rows:
        # 检查是否已存在同名Source
        result = await local_session.execute(
            select(MediaItem).where(MediaItem.Name == row['Name'], MediaItem.Type == MediaType.Source)
        )
        existing = result.scalar_one_or_none()
        
        if existing:
            id_mapping[row['Id']] = existing.Id
            continue
        
        item = MediaItem(
            Type=MediaType.Source,
            Name=row['Name'],
            Overview=row['Description'] or f"来自 {row['Name']}",
            IsDeleted=False,
            DateCreated=datetime.utcnow(),
            DateModified=datetime.utcnow(),
        )
        local_session.add(item)
        await local_session.flush()
        id_mapping[row['Id']] = item.Id
    
    await local_session.commit()
    stats.record("Providers→Source", len(id_mapping))
    return id_mapping


async def migrate_media_items(remote_conn, local_session, provider_mapping):
    """迁移 MediaItems"""
    print("\n🎬 迁移 MediaItems...")
    
    # 分批获取
    batch_size = 1000
    offset = 0
    total_migrated = 0
    
    while True:
        rows = await remote_conn.fetch(
            '''SELECT "Id", "Type", "Name", "OriginalTitle", "SortName", 
               "Overview", "Tagline", "PremiereDate", "EndDate",
               "OfficialRating", "CommunityRating", "CriticRating",
               "DateCreated", "DateModified", "IsDeleted"
               FROM "MediaItems" 
               WHERE "IsDeleted" = false
               ORDER BY "Id" LIMIT $1 OFFSET $2''',
            batch_size, offset
        )
        
        if not rows:
            break
        
        for row in rows:
            media_type = MEDIA_TYPE_MAP.get(row['Type'])
            if not media_type:
                continue
            
            item = MediaItem(
                Id=row['Id'],  # 保持原ID
                Type=media_type,
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
            local_session.add(item)
        
        await local_session.commit()
        total_migrated += len(rows)
        offset += batch_size
        print(f"  进度: {total_migrated} 条", end='\r')
    
    print()
    stats.record("MediaItems", total_migrated)


async def migrate_files(remote_conn, local_session):
    """迁移 Files"""
    print("\n📁 迁移 Files...")
    
    batch_size = 1000
    offset = 0
    total_migrated = 0
    
    while True:
        rows = await remote_conn.fetch(
            '''SELECT "Id", "Etag", "Size", "Name", "SortName", 
               "Path", "CloudId", "Type", "Data"
               FROM "Files" 
               ORDER BY "Id" LIMIT $1 OFFSET $2''',
            batch_size, offset
        )
        
        if not rows:
            break
        
        for row in rows:
            file_type = FILE_TYPE_MAP.get(row['Type'], FileType.Video)
            
            # 提取 FFmpeg 信息
            ffmpeg_info = None
            if row['Data']:
                try:
                    data = json.loads(row['Data'])
                    ffmpeg_info = json.dumps(data, ensure_ascii=False)
                except:
                    pass
            
            file = File(
                Id=row['Id'],
                Etag=row['Etag'],
                Size=row['Size'],
                Name=row['Name'],
                SortName=row['SortName'],
                Path=row['Path'],
                CloudId=row['CloudId'],
                Type=file_type,
                FFmpeg=ffmpeg_info,
            )
            local_session.add(file)
        
        await local_session.commit()
        total_migrated += len(rows)
        offset += batch_size
        print(f"  进度: {total_migrated} 条", end='\r')
    
    print()
    stats.record("Files", total_migrated)


async def migrate_item_links(remote_conn, local_session):
    """迁移 ItemLinks"""
    print("\n🔗 迁移 ItemLinks...")
    
    batch_size = 2000
    offset = 0
    total_migrated = 0
    
    while True:
        rows = await remote_conn.fetch(
            '''SELECT "ItemId", "LinkedItemId", "Order"
               FROM "ItemLinks" 
               ORDER BY "ItemId", "LinkedItemId" LIMIT $1 OFFSET $2''',
            batch_size, offset
        )
        
        if not rows:
            break
        
        for row in rows:
            link = ItemLinks(
                ItemId=row['ItemId'],
                LinkedItemId=row['LinkedItemId'],
                Type=LinkType.Season,  # 默认类型，可根据业务调整
            )
            local_session.add(link)
        
        await local_session.commit()
        total_migrated += len(rows)
        offset += batch_size
        print(f"  进度: {total_migrated} 条", end='\r')
    
    print()
    stats.record("ItemLinks", total_migrated)


async def migrate_item_people(remote_conn, local_session):
    """迁移 ItemPeople → ItemLinks"""
    print("\n👥 迁移 ItemPeople → ItemLinks...")
    
    batch_size = 2000
    offset = 0
    total_migrated = 0
    
    # PeopleType 映射
    people_type_map = {
        'Actor': PeopleType.Actor,
        'Director': PeopleType.Director,
        'Writer': PeopleType.Writer,
        'Producer': PeopleType.Producer,
    }
    
    while True:
        rows = await remote_conn.fetch(
            '''SELECT "ItemId", "PersonId", "Role", "Type", "Order"
               FROM "ItemPeople" 
               ORDER BY "ItemId", "PersonId" LIMIT $1 OFFSET $2''',
            batch_size, offset
        )
        
        if not rows:
            break
        
        for row in rows:
            people_type = people_type_map.get(row['Type'], PeopleType.Actor)
            
            link = ItemLinks(
                ItemId=row['ItemId'],
                LinkedItemId=row['PersonId'],
                Type=LinkType.Person,
                PeopleType=people_type,
                PeopleRole=row['Role'],
            )
            local_session.add(link)
        
        await local_session.commit()
        total_migrated += len(rows)
        offset += batch_size
        print(f"  进度: {total_migrated} 条", end='\r')
    
    print()
    stats.record("ItemPeople→Links", total_migrated)


async def migrate_file_images(remote_conn, local_session):
    """迁移 FileImages → FileLinks"""
    print("\n🖼️  迁移 FileImages → FileLinks...")
    
    batch_size = 2000
    offset = 0
    total_migrated = 0
    
    # ImageType 映射
    image_type_map = {
        'Primary': ImageType.Primary,
        'Backdrop': ImageType.Backdrop,
        'Logo': ImageType.Logo,
        'Thumb': ImageType.Thumb,
    }
    
    while True:
        rows = await remote_conn.fetch(
            '''SELECT "ItemId", "FileId", "Type", "ImageIndex"
               FROM "FileImages" 
               ORDER BY "ItemId", "FileId" LIMIT $1 OFFSET $2''',
            batch_size, offset
        )
        
        if not rows:
            break
        
        for row in rows:
            image_type = image_type_map.get(row['Type'], ImageType.Primary)
            
            link = FileLink(
                ItemId=row['ItemId'],
                FileId=row['FileId'],
                ImageType=image_type,
                ImageIndex=row['ImageIndex'] or 0,
            )
            local_session.add(link)
        
        await local_session.commit()
        total_migrated += len(rows)
        offset += batch_size
        print(f"  进度: {total_migrated} 条", end='\r')
    
    print()
    stats.record("FileImages→Links", total_migrated)


async def migrate_item_sources(remote_conn, local_session, provider_mapping):
    """迁移 ItemSources → ItemLinks"""
    print("\n📡 迁移 ItemSources → ItemLinks...")
    
    batch_size = 2000
    offset = 0
    total_migrated = 0
    
    while True:
        rows = await remote_conn.fetch(
            '''SELECT "ItemId", "ProviderId", "Url"
               FROM "ItemSources" 
               ORDER BY "ItemId" LIMIT $1 OFFSET $2''',
            batch_size, offset
        )
        
        if not rows:
            break
        
        for row in rows:
            # 映射 ProviderId 到新的 Source MediaItem Id
            source_id = provider_mapping.get(row['ProviderId'])
            if not source_id:
                continue
            
            link = ItemLinks(
                ItemId=row['ItemId'],
                LinkedItemId=source_id,
                Type=LinkType.Source,
            )
            local_session.add(link)
        
        await local_session.commit()
        total_migrated += len(rows)
        offset += batch_size
        print(f"  进度: {total_migrated} 条", end='\r')
    
    print()
    stats.record("ItemSources→Links", total_migrated)


async def main():
    print("="*60)
    print("核心数据迁移工具")
    print("="*60)
    print(f"远程数据库: {REMOTE_DB_CONFIG['host']}")
    print(f"本地数据库: SQLite/PostgreSQL")
    print()
    
    # 连接远程数据库
    print("🔗 连接远程 PostgreSQL...")
    remote_conn = await asyncpg.connect(**REMOTE_DB_CONFIG)
    print("✅ 连接成功")
    
    # 创建本地会话
    async with AsyncSessionLocal() as local_session:
        # 清理现有数据（可选）
        print("\n⚠️  是否清理现有数据? (y/N): ", end='')
        # 默认不清理，如需清理可手动执行
        
        # 1. 迁移 Providers → Source
        provider_mapping = await migrate_providers(remote_conn, local_session)
        
        # 2. 迁移 MediaItems
        await migrate_media_items(remote_conn, local_session, provider_mapping)
        
        # 3. 迁移 Files
        await migrate_files(remote_conn, local_session)
        
        # 4. 迁移 ItemLinks
        await migrate_item_links(remote_conn, local_session)
        
        # 5. 迁移 ItemPeople → ItemLinks
        await migrate_item_people(remote_conn, local_session)
        
        # 6. 迁移 FileImages → FileLinks
        await migrate_file_images(remote_conn, local_session)
        
        # 7. 迁移 ItemSources → ItemLinks
        await migrate_item_sources(remote_conn, local_session, provider_mapping)
    
    await remote_conn.close()
    
    # 显示统计
    stats.show_summary()
    
    print("\n✅ 迁移完成！")


if __name__ == '__main__':
    asyncio.run(main())
