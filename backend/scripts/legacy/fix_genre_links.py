"""补全 Genre 关联关系"""
import os
import asyncio
import asyncpg
from database.core import AsyncSessionLocal
from database.models import ItemLinks
from sqlalchemy import select


async def fix_genre_links():
    # 连接远程
    conn = await asyncpg.connect(
        host=os.environ.get('REMOTE_DB_HOST', ''),
        port=int(os.environ.get('REMOTE_DB_PORT', '5432')),
        database=os.environ.get('REMOTE_DB_NAME', ''),
        user=os.environ.get('REMOTE_DB_USER', ''),
        password=os.environ.get('REMOTE_DB_PASSWORD', '')
    )

    # 获取所有 Genre ID
    genres = await conn.fetch('SELECT "Id" FROM "MediaItems" WHERE "Type" = $1', 'Genre')
    genre_ids = [r['Id'] for r in genres]
    print(f"需要补全关联的 Genre: {len(genre_ids)} 个")

    async with AsyncSessionLocal() as s:
        total_created = 0
        for genre_id in genre_ids:
            # 获取远程关联关系
            links = await conn.fetch('''
                SELECT il."ItemId", il."LinkedItemId"
                FROM "ItemLinks" il
                JOIN "ItemProviders" ip ON il."ItemId" = ip."ItemId"
                WHERE il."LinkedItemId" = $1 AND ip."ProviderId" = 1
            ''', genre_id)

            print(f"\nGenre {genre_id}: 远程有 {len(links)} 个关联")

            for link_data in links:
                # 检查本地是否已存在
                result = await s.execute(
                    select(ItemLinks).where(
                        ItemLinks.ItemId == link_data['ItemId'],
                        ItemLinks.LinkedItemId == link_data['LinkedItemId'],
                        ItemLinks.Type == 'Genre'
                    )
                )
                existing = result.scalar_one_or_none()

                if existing:
                    continue

                # 创建关联
                link = ItemLinks(
                    ItemId=link_data['ItemId'],
                    LinkedItemId=link_data['LinkedItemId'],
                    Type='Genre',
                )
                s.add(link)
                total_created += 1

                if total_created % 500 == 0:
                    await s.commit()
                    print(f"  已创建 {total_created} 个关联")

            await s.commit()

        print(f"\n✅ 共补全 {total_created} 个 Genre 关联")

    await conn.close()


asyncio.run(fix_genre_links())
