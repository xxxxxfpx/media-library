import asyncio
from database.core import AsyncSessionLocal, engine
from database.models import ItemLinks, FileLink, MediaItem
from sqlalchemy import delete, text

async def clean():
    async with engine.begin() as conn:
        await conn.execute(delete(ItemLinks).where(ItemLinks.ItemId == 3102))
        await conn.execute(delete(FileLink).where(FileLink.ItemId == 3102))
        await conn.execute(delete(MediaItem).where(MediaItem.Id == 3102))
        print('已彻底清理 ID=3102 的所有数据')

asyncio.run(clean())
