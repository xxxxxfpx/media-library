"""补全缺失的 Genre"""
import os
import asyncio
import asyncpg
from datetime import datetime, timezone, timedelta
from database.core import AsyncSessionLocal
from database.models import MediaItem, MediaType
from sqlalchemy import select


async def fix_genres():
    # 连接远程
    conn = await asyncpg.connect(
        host=os.environ.get('REMOTE_DB_HOST', ''),
        port=int(os.environ.get('REMOTE_DB_PORT', '5432')),
        database=os.environ.get('REMOTE_DB_NAME', ''),
        user=os.environ.get('REMOTE_DB_USER', ''),
        password=os.environ.get('REMOTE_DB_PASSWORD', '')
    )

    # 获取所有 Genre
    rows = await conn.fetch(
        'SELECT "Id", "Name" FROM "MediaItems" WHERE "Type" = $1',
        'Genre'
    )
    print(f'远程 Genre 总数: {len(rows)}')

    async with AsyncSessionLocal() as s:
        for row in rows:
            # 检查本地是否存在
            result = await s.execute(
                select(MediaItem).where(MediaItem.Id == row['Id'])
            )
            existing = result.scalar_one_or_none()
            if existing:
                print(f'  已存在: Id={row["Id"]}, Name={row["Name"]}')
                continue

            # 创建
            item = MediaItem(
                Id=row['Id'],
                Type=MediaType.Genre,
                Name=row['Name'],
                DateCreated=datetime.now(timezone(timedelta(hours=8))),
                DateModified=datetime.now(timezone(timedelta(hours=8))),
            )
            s.add(item)
            await s.flush()
            print(f'  创建: Id={row["Id"]}, Name={row["Name"]}')

        await s.commit()

    # 验证
    async with AsyncSessionLocal() as s:
        result = await s.execute(select(MediaItem).where(MediaItem.Type == 'Genre'))
        items = result.scalars().all()
        print(f'\n本地 Genre 最终数量: {len(items)}')

    await conn.close()


asyncio.run(fix_genres())
