"""检查数据库中的 Season 和 Series 数量"""
import asyncio
import sys

try:
    from database.core import AsyncSessionLocal
    from database.models import MediaItem
    from sqlalchemy import select, func
except Exception as e:
    print(f"导入错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)


async def check():
    try:
        async with AsyncSessionLocal() as s:
            print("=== 本地数据库统计 ===")
            for t in ['Season', 'Series', 'Episode']:
                count = (await s.execute(select(func.count()).where(MediaItem.Type == t))).scalar_one()
                print(f'{t}: {count}')
    except Exception as e:
        print(f"查询错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    asyncio.run(check())
