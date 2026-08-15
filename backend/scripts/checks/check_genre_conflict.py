"""检查 Genre 名称冲突"""
import asyncio
from database.core import AsyncSessionLocal
from database.models import MediaItem
from sqlalchemy import select


async def check():
    async with AsyncSessionLocal() as s:
        # 所有已存在的媒体项名称
        result = await s.execute(select(MediaItem.Name, MediaItem.Type))
        items = result.all()
        
        # 检查远程的 Genre 名称是否冲突
        genres = [
            (41, '里番'),
            (6928, '2.5D'),
            (17262, 'AI生成'),
            (12507, '2D动画'),
            (541, 'Motion Anime'),
            (827, '3DCG'),
            (22997, 'MMD'),
            (23306, 'Cosplay'),
            (23650, '泡面番'),
        ]
        
        existing_names = {name: type_ for name, type_ in items if name}
        
        print("检查 Genre 名称冲突:")
        for gid, gname in genres:
            if gname in existing_names:
                print(f"  ⚠️  {gname} 已存在，类型={existing_names[gname]}")
            else:
                print(f"  ✅ {gname} 可用")


asyncio.run(check())
