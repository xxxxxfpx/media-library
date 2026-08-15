"""检查本地数据库 Genre"""
import asyncio
from database.core import AsyncSessionLocal
from database.models import MediaItem
from sqlalchemy import select


async def check():
    async with AsyncSessionLocal() as s:
        result = await s.execute(select(MediaItem).where(MediaItem.Type == 'Genre'))
        items = result.scalars().all()
        print(f'本地 Genre 数量: {len(items)}')
        for item in items:
            print(f'  Id={item.Id}, Name={item.Name}')


asyncio.run(check())
