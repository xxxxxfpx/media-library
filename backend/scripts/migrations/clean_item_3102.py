import asyncio
from database.core import AsyncSessionLocal
from database.models import ItemLinks, FileLink
from sqlalchemy import delete

async def clean():
    async with AsyncSessionLocal() as session:
        await session.execute(delete(ItemLinks).where(ItemLinks.ItemId == 3102))
        await session.execute(delete(FileLink).where(FileLink.ItemId == 3102))
        await session.commit()
        print('已清理 ID=3102 的关联数据')

asyncio.run(clean())
