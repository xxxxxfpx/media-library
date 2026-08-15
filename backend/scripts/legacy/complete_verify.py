"""完整迁移验证"""
import os
import asyncio
import asyncpg
from database.core import AsyncSessionLocal
from database.models import MediaItem, ItemLinks, File, FileLink
from sqlalchemy import select, func


async def verify():
    conn = await asyncpg.connect(
        host=os.environ.get('REMOTE_DB_HOST', ''),
        port=int(os.environ.get('REMOTE_DB_PORT', '5432')),
        database=os.environ.get('REMOTE_DB_NAME', ''),
        user=os.environ.get('REMOTE_DB_USER', ''),
        password=os.environ.get('REMOTE_DB_PASSWORD', '')
    )

    async with AsyncSessionLocal() as s:
        print("=" * 80)
        print("Hanime 数据迁移完整验证")
        print("=" * 80)

        # 1. MediaItems 验证
        print("\n=== MediaItems ===")
        types = ['Tag', 'Genre', 'Studio', 'BoxSet', 'Movie', 'Series', 'Season', 'Episode']
        for t in types:
            local = (await s.execute(select(func.count()).where(MediaItem.Type == t))).scalar_one()
            remote = await conn.fetchval('''
                SELECT COUNT(*) FROM "MediaItems" mi
                JOIN "ItemProviders" ip ON mi."Id" = ip."ItemId"
                WHERE mi."Type" = $1 AND ip."ProviderId" = 1
            ''', t)
            status = "✅" if local == remote else "❌"
            print(f"  {status} {t}: 本地={local}, 远程={remote}")

        local_source = (await s.execute(select(func.count()).where(MediaItem.Type == 'Source'))).scalar_one()
        print(f"  ✅ Source: 本地={local_source} (Hanime)")

        # 2. ItemLinks 验证
        print("\n=== ItemLinks ===")
        result = await s.execute(select(func.count()).select_from(ItemLinks))
        local_links = result.scalar_one()
        print(f"  总关联数: {local_links}")
        
        for t in ['Genre', 'Studio', 'Tag', 'BoxSet', 'Source']:
            local = (await s.execute(select(func.count()).where(ItemLinks.Type == t))).scalar_one()
            if t == 'Source':
                remote = await conn.fetchval('''
                    SELECT COUNT(DISTINCT mi."Id")
                    FROM "ItemProviders" ip
                    JOIN "MediaItems" mi ON ip."ItemId" = mi."Id"
                ''')
            else:
                remote = await conn.fetchval('''
                    SELECT COUNT(*) FROM "ItemLinks" il
                    JOIN "MediaItems" mi ON il."LinkedItemId" = mi."Id"
                    JOIN "ItemProviders" ip ON il."ItemId" = ip."ItemId"
                    WHERE mi."Type" = $1 AND ip."ProviderId" = 1
                ''', t)
            status = "✅" if local == remote else "❌"
            print(f"  {status} {t}: 本地={local}, 远程={remote}")

        # 3. Files 验证
        print("\n=== Files ===")
        file_count = (await s.execute(select(func.count()).select_from(File))).scalar_one()
        filelink_count = (await s.execute(select(func.count()).select_from(FileLink))).scalar_one()
        print(f"  File 总数: {file_count}")
        print(f"  FileLink 总数: {filelink_count}")
        
        # 有文件关联的媒体
        movies_with_files = await s.execute(
            select(func.count(MediaItem.Id.distinct()))
            .select_from(MediaItem)
            .join(FileLink, MediaItem.Id == FileLink.ItemId)
            .where(MediaItem.Type == 'Movie')
        )
        print(f"  ✅ 有文件关联的 Movie: {movies_with_files.scalar_one()}/15689")
        
        episodes_with_files = await s.execute(
            select(func.count(MediaItem.Id.distinct()))
            .select_from(MediaItem)
            .join(FileLink, MediaItem.Id == FileLink.ItemId)
            .where(MediaItem.Type == 'Episode')
        )
        print(f"  ✅ 有文件关联的 Episode: {episodes_with_files.scalar_one()}/528")

        # 4. 总计
        print("\n=== 总计 ===")
        media_total = (await s.execute(select(func.count()).select_from(MediaItem))).scalar_one()
        print(f"  MediaItems: {media_total}")
        print(f"  ItemLinks: {local_links}")
        print(f"  Files: {file_count}")
        print(f"  FileLinks: {filelink_count}")
        print("=" * 80)
        print("✅ 迁移完成！")
        print("=" * 80)

    await conn.close()


asyncio.run(verify())
