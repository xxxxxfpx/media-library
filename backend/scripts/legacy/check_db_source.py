"""检查数据库中的 Source 关联"""
import asyncio
from database.core import AsyncSessionLocal
from database.models import ItemLinks, ItemLinkType
from sqlalchemy import select

async def check():
    async with AsyncSessionLocal() as session:
        # 检查 ID=3102 的 Source 类型关联
        result = await session.execute(
            select(ItemLinks).where(
                ItemLinks.ItemId == 3102,
                ItemLinks.Type == ItemLinkType.Source
            )
        )
        links = result.scalars().all()
        
        print(f"ID=3102 的 Source 关联数量: {len(links)}")
        for link in links:
            print(f"  LinkedItemId={link.LinkedItemId}, Type={link.Type}")
        
        # 检查所有 ItemLinks
        result = await session.execute(
            select(ItemLinks).where(ItemLinks.ItemId == 3102)
        )
        all_links = result.scalars().all()
        print(f"\nID=3102 的所有关联数量: {len(all_links)}")
        
        from database.models import MediaItem
        for link in all_links:
            result = await session.execute(
                select(MediaItem).where(MediaItem.Id == link.LinkedItemId)
            )
            item = result.scalar_one_or_none()
            if item:
                print(f"  {link.Type.value}: {item.Name} (ID={item.Id})")
            else:
                print(f"  {link.Type.value}: LinkedItemId={link.LinkedItemId} (未找到)")

asyncio.run(check())
