"""验证 Hanime 迁移结果"""
import asyncio
from database.core import AsyncSessionLocal
from database.models import MediaItem, ItemLinks, MediaType
from sqlalchemy import select, func


async def check():
    async with AsyncSessionLocal() as s:
        print("="*60)
        print("Hanime 迁移结果验证")
        print("="*60)
        
        types = ['Tag', 'Genre', 'Studio', 'BoxSet', 'Movie', 'Series', 'Season', 'Episode']
        print("\n=== MediaItems 统计 ===")
        for t in types:
            count = (await s.execute(select(func.count()).where(MediaItem.Type == t))).scalar_one()
            print(f"  {t}: {count}")
        
        source_count = (await s.execute(select(func.count()).where(MediaItem.Type == MediaType.Source))).scalar_one()
        print(f"  Source: {source_count}")
        
        total = (await s.execute(select(func.count(MediaItem)))).scalar_one()
        print(f"\n  MediaItems 总计: {total}")
        
        print("\n=== ItemLinks 统计 ===")
        total_links = (await s.execute(select(func.count(ItemLinks)))).scalar_one()
        print(f"  总关联数: {total_links}")
        
        for t in ['Source', 'Tag', 'Genre', 'Studio', 'BoxSet', 'Season', 'Episode']:
            count = (await s.execute(select(func.count()).where(ItemLinks.Type == t))).scalar_one()
            print(f"  {t}: {count}")
        
        print("\n✅ 验证完成")


asyncio.run(check())
