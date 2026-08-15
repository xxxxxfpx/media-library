"""
迁移单个视频及其伴生属性
"""
import os
import asyncio
import asyncpg
from datetime import datetime
from database.core import AsyncSessionLocal
from database.models import (
    MediaItem, MediaType, ItemLinks, ItemLinkType,
    FileLink, ImageType, PersonType
)
from sqlalchemy import select

REMOTE_DB_CONFIG = {
    'host': os.environ.get('REMOTE_DB_HOST', ''),
    'port': int(os.environ.get('REMOTE_DB_PORT', '5432')),
    'database': os.environ.get('REMOTE_DB_NAME', ''),
    'user': os.environ.get('REMOTE_DB_USER', ''),
    'password': os.environ.get('REMOTE_DB_PASSWORD', '')
}


async def migrate_movie_and_associations(remote_item_id):
    """迁移单个视频及其所有伴生属性"""
    print(f"\n{'='*60}")
    print(f"迁移远程视频 ID={remote_item_id} 及其伴生属性")
    print(f"{'='*60}")
    
    # 连接远程数据库
    remote_conn = await asyncpg.connect(**REMOTE_DB_CONFIG)
    
    async with AsyncSessionLocal() as local_session:
        # 1. 获取远程视频信息
        row = await remote_conn.fetchrow(
            '''SELECT "Id", "Name", "OriginalTitle", "SortName", 
               "Overview", "Tagline", "PremiereDate", "EndDate",
               "OfficialRating", "CommunityRating", "CriticRating",
               "DateCreated", "DateModified"
               FROM "MediaItems" WHERE "Id" = $1''',
            remote_item_id
        )
        
        if not row:
            print(f"❌ 远程数据库中不存在 ID={remote_item_id}")
            await remote_conn.close()
            return False
        
        print(f"📺 视频名称: {row['Name']}")
        
        # 检查本地是否已存在
        result = await local_session.execute(
            select(MediaItem).where(MediaItem.Id == remote_item_id)
        )
        existing = result.scalar_one_or_none()
        
        if existing:
            print(f"⚠️ 本地已存在 ID={remote_item_id}，跳过媒体迁移")
            media_item = existing
        else:
            # 创建本地媒体项
            media_item = MediaItem(
                Id=row['Id'],
                Type=MediaType.Movie,
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
                IsDeleted=False,
            )
            local_session.add(media_item)
            await local_session.commit()
            print(f"✅ 媒体项迁移完成")
        
        # 2. 迁移 ItemLinks
        print(f"\n🔗 迁移 ItemLinks...")
        links = await remote_conn.fetch(
            'SELECT "LinkedItemId", "Order" FROM "ItemLinks" WHERE "ItemId" = $1',
            remote_item_id
        )
        for link in links:
            # ItemLinks 通用关联使用 Source 类型
            l = ItemLinks(
                ItemId=remote_item_id,
                LinkedItemId=link['LinkedItemId'],
                Type=ItemLinkType.Source,
            )
            local_session.add(l)
        await local_session.commit()
        print(f"  ✅ {len(links)} 条关联")
        
        # 3. 迁移 ItemPeople
        print(f"\n👥 迁移 ItemPeople...")
        people = await remote_conn.fetch(
            'SELECT "PersonId", "Role", "Type" FROM "ItemPeople" WHERE "ItemId" = $1',
            remote_item_id
        )
        people_type_map = {'Actor': PersonType.Actor, 'Director': PersonType.Director, 
                          'Writer': PersonType.Writer, 'Producer': PersonType.Producer}
        for p in people:
            l = ItemLinks(
                ItemId=remote_item_id,
                LinkedItemId=p['PersonId'],
                Type=ItemLinkType.Person,
                PeopleType=people_type_map.get(p['Type'], PersonType.Actor),
                PeopleRole=p['Role'],
            )
            local_session.add(l)
        await local_session.commit()
        print(f"  ✅ {len(people)} 个人物关联")
        
        # 4. 迁移 FileImages
        print(f"\n🖼️ 迁移 FileImages...")
        images = await remote_conn.fetch(
            'SELECT "FileId", "Type", "ImageIndex" FROM "FileImages" WHERE "ItemId" = $1',
            remote_item_id
        )
        image_type_map = {'Primary': ImageType.Primary, 'Backdrop': ImageType.Backdrop,
                         'Logo': ImageType.Logo, 'Thumb': ImageType.Thumb}
        for img in images:
            fl = FileLink(
                ItemId=remote_item_id,
                FileId=img['FileId'],
                ImageType=image_type_map.get(img['Type'], ImageType.Primary),
                ImageIndex=img['ImageIndex'] or 0,
            )
            local_session.add(fl)
        await local_session.commit()
        print(f"  ✅ {len(images)} 个文件图片")
        
        # 5. 统计
        total = len(links) + len(people) + len(images)
        print(f"\n{'='*60}")
        print("迁移完成统计")
        print(f"{'='*60}")
        print(f"  ItemLinks:    {len(links)}")
        print(f"  ItemPeople:   {len(people)}")
        print(f"  FileImages:   {len(images)}")
        print(f"  总计:         {total}")
    
    await remote_conn.close()
    return True


async def main():
    # 使用 ID=3102 测试
    await migrate_movie_and_associations(3102)
    print(f"\n✅ 迁移完成！")


if __name__ == '__main__':
    asyncio.run(main())
