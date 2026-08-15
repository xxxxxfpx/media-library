"""补全缺失的 Studio、BoxSet 和 Movie 数据"""
import os
import asyncio
import asyncpg
from datetime import datetime, timezone, timedelta
from database.core import AsyncSessionLocal
from database.models import MediaItem, MediaType
from sqlalchemy import select


def to_local_time(dt):
    """将时间转换为 UTC+8 时区"""
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone(timedelta(hours=8)))
    return dt.astimezone(timezone(timedelta(hours=8)))


async def fill_missing_data():
    conn = await asyncpg.connect(
        host=os.environ.get('REMOTE_DB_HOST', ''),
        port=int(os.environ.get('REMOTE_DB_PORT', '5432')),
        database=os.environ.get('REMOTE_DB_NAME', ''),
        user=os.environ.get('REMOTE_DB_USER', ''),
        password=os.environ.get('REMOTE_DB_PASSWORD', '')
    )

    async with AsyncSessionLocal() as s:
        # 1. 补全 Studio
        print("\n=== 补全 Studio ===")
        remote_studios = await conn.fetch('''
            SELECT mi."Id", mi."Name", mi."Overview", mi."DateCreated", mi."DateModified"
            FROM "MediaItems" mi
            JOIN "ItemProviders" ip ON mi."Id" = ip."ItemId"
            WHERE mi."Type" = 'Studio' AND ip."ProviderId" = 1
        ''')
        
        result = await s.execute(select(MediaItem.Id).where(MediaItem.Type == 'Studio'))
        local_studio_ids = {row[0] for row in result.all()}
        
        missing_studios = [r for r in remote_studios if r['Id'] not in local_studio_ids]
        print(f"远程: {len(remote_studios)}, 本地: {len(local_studio_ids)}, 缺失: {len(missing_studios)}")
        
        created = 0
        for studio in missing_studios:
            item = MediaItem(
                Id=studio['Id'],
                Type=MediaType.Studio,
                Name=studio['Name'],
                Overview=studio['Overview'],
                DateCreated=to_local_time(studio['DateCreated']),
                DateModified=to_local_time(studio['DateModified']),
            )
            s.add(item)
            created += 1
            if created % 100 == 0:
                await s.commit()
        
        await s.commit()
        print(f"✅ 补全 {created} 个 Studio")

        # 2. 补全 BoxSet
        print("\n=== 补全 BoxSet ===")
        remote_boxsets = await conn.fetch('''
            SELECT mi."Id", mi."Name", mi."Overview", mi."DateCreated", mi."DateModified"
            FROM "MediaItems" mi
            JOIN "ItemProviders" ip ON mi."Id" = ip."ItemId"
            WHERE mi."Type" = 'BoxSet' AND ip."ProviderId" = 1
        ''')
        
        result = await s.execute(select(MediaItem.Id).where(MediaItem.Type == 'BoxSet'))
        local_boxset_ids = {row[0] for row in result.all()}
        
        missing_boxsets = [r for r in remote_boxsets if r['Id'] not in local_boxset_ids]
        print(f"远程: {len(remote_boxsets)}, 本地: {len(local_boxset_ids)}, 缺失: {len(missing_boxsets)}")
        
        created = 0
        for boxset in missing_boxsets:
            item = MediaItem(
                Id=boxset['Id'],
                Type=MediaType.BoxSet,
                Name=boxset['Name'],
                Overview=boxset['Overview'],
                DateCreated=to_local_time(boxset['DateCreated']),
                DateModified=to_local_time(boxset['DateModified']),
            )
            s.add(item)
            created += 1
            if created % 100 == 0:
                await s.commit()
        
        await s.commit()
        print(f"✅ 补全 {created} 个 BoxSet")

        # 3. 补全 Movie
        print("\n=== 补全 Movie ===")
        remote_movies = await conn.fetch('''
            SELECT mi."Id", mi."Name", mi."Overview", mi."Tagline",
                   mi."PremiereDate", mi."OfficialRating", mi."CommunityRating",
                   mi."DateCreated", mi."DateModified"
            FROM "MediaItems" mi
            JOIN "ItemProviders" ip ON mi."Id" = ip."ItemId"
            WHERE mi."Type" = 'Movie' AND ip."ProviderId" = 1
        ''')
        
        result = await s.execute(select(MediaItem.Id).where(MediaItem.Type == 'Movie'))
        local_movie_ids = {row[0] for row in result.all()}
        
        missing_movies = [r for r in remote_movies if r['Id'] not in local_movie_ids]
        print(f"远程: {len(remote_movies)}, 本地: {len(local_movie_ids)}, 缺失: {len(missing_movies)}")
        
        created = 0
        for movie in missing_movies:
            item = MediaItem(
                Id=movie['Id'],
                Type=MediaType.Movie,
                Name=movie['Name'],
                Overview=movie['Overview'],
                Tagline=movie['Tagline'],
                PremiereDate=movie['PremiereDate'],
                OfficialRating=movie['OfficialRating'],
                CommunityRating=movie['CommunityRating'],
                DateCreated=to_local_time(movie['DateCreated']),
                DateModified=to_local_time(movie['DateModified']),
            )
            s.add(item)
            created += 1
            if created % 100 == 0:
                await s.commit()
        
        await s.commit()
        print(f"✅ 补全 {created} 个 Movie")

    await conn.close()
    
    # 验证最终结果
    print("\n=== 最终验证 ===")
    async with AsyncSessionLocal() as s:
        for t in ['Studio', 'BoxSet', 'Movie']:
            local = (await s.execute(select(func.count()).where(MediaItem.Type == t))).scalar_one()
            print(f"  {t}: {local}")


if __name__ == "__main__":
    from sqlalchemy import func
    asyncio.run(fill_missing_data())
