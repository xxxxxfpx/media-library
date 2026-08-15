"""验证 Genre 关联关系 - 修复版"""
import os
import asyncio
import asyncpg
from database.core import AsyncSessionLocal
from database.models import MediaItem, ItemLinks
from sqlalchemy import select, func


async def check():
    async with AsyncSessionLocal() as s:
        # 1. 获取本地所有 Genre
        result = await s.execute(select(MediaItem.Id, MediaItem.Name).where(MediaItem.Type == 'Genre'))
        local_genres = {row.Id: row.Name for row in result.all()}
        print(f"本地 Genre: {len(local_genres)} 个")
        for gid, gname in local_genres.items():
            print(f"  Id={gid}, Name={gname}")
        
        # 2. 检查每个 Genre 有多少个关联
        print("\n=== 本地 Genre 关联统计 ===")
        total_local_links = 0
        for gid, gname in local_genres.items():
            count = (await s.execute(
                select(func.count()).where(
                    ItemLinks.LinkedItemId == gid,
                    ItemLinks.Type == 'Genre'
                )
            )).scalar_one()
            print(f"  {gname}: {count} 个关联")
            total_local_links += count
        print(f"\n本地 Genre 关联总数: {total_local_links}")
        
        # 3. 对比远程数据库的关联数（ItemLinks 没有 Type 字段，需要通过 MediaItems.Type 过滤）
        conn = await asyncpg.connect(
            host=os.environ.get('REMOTE_DB_HOST', ''),
            port=int(os.environ.get('REMOTE_DB_PORT', '5432')),
            database=os.environ.get('REMOTE_DB_NAME', ''),
            user=os.environ.get('REMOTE_DB_USER', ''),
            password=os.environ.get('REMOTE_DB_PASSWORD', '')
        )
        
        print("\n=== 远程 Hanime Genre 关联统计 ===")
        total_remote_links = 0
        for gid, gname in local_genres.items():
            remote_count = await conn.fetchval('''
                SELECT COUNT(*) FROM "ItemLinks" il
                JOIN "ItemProviders" ip ON il."ItemId" = ip."ItemId"
                JOIN "MediaItems" mi ON il."LinkedItemId" = mi."Id"
                WHERE il."LinkedItemId" = $1 AND mi."Type" = 'Genre' AND ip."ProviderId" = 1
            ''', gid)
            print(f"  {gname} (Id={gid}): {remote_count} 个关联")
            total_remote_links += remote_count
        print(f"\n远程 Genre 关联总数: {total_remote_links}")
        
        await conn.close()


asyncio.run(check())
