"""
修复 ItemLinks 关联方向
将层级关联从"父级→子级"改为"子级→父级"
- Series → Season (Type='Season') 变成 Season → Series (Type='Season')
- Season → Episode (Type='Episode') 变成 Episode → Season (Type='Episode')

Type 值保持不变，因为 Type 表示的是被交换的 ItemId 的原类型
"""
import asyncio
from database.core import AsyncSessionLocal
from database.models import ItemLinks
from sqlalchemy import select


async def fix_itemlinks_direction():
    """修复 ItemLinks 的关联方向"""
    print("=" * 60)
    print("修复 ItemLinks 关联方向")
    print("=" * 60)

    async with AsyncSessionLocal() as s:
        # 1. 修复 Season → Series 关联 (Type='Season')
        print("\n=== 修复 Season → Series 关联 ===")

        result = await s.execute(
            select(ItemLinks).where(ItemLinks.Type == 'Season')
        )
        season_links = result.scalars().all()
        print(f"找到 {len(season_links)} 条 Type='Season' 的关联")

        fixed_season = 0
        for link in season_links:
            old_item_id = link.ItemId
            old_linked_id = link.LinkedItemId
            link.ItemId = old_linked_id
            link.LinkedItemId = old_item_id
            fixed_season += 1

            if fixed_season % 1000 == 0:
                await s.commit()
                print(f"  已处理 {fixed_season} 条")

        await s.commit()
        print(f"✅ 修复了 {fixed_season} 条 Season 关联")

        # 2. 修复 Episode → Season 关联 (Type='Episode')
        print("\n=== 修复 Episode → Season 关联 ===")

        result = await s.execute(
            select(ItemLinks).where(ItemLinks.Type == 'Episode')
        )
        episode_links = result.scalars().all()
        print(f"找到 {len(episode_links)} 条 Type='Episode' 的关联")

        fixed_episode = 0
        for link in episode_links:
            old_item_id = link.ItemId
            old_linked_id = link.LinkedItemId
            link.ItemId = old_linked_id
            link.LinkedItemId = old_item_id
            fixed_episode += 1

            if fixed_episode % 1000 == 0:
                await s.commit()
                print(f"  已处理 {fixed_episode} 条")

        await s.commit()
        print(f"✅ 修复了 {fixed_episode} 条 Episode 关联")

        # 3. 验证修复结果
        print("\n=== 验证修复结果 ===")

        result = await s.execute(
            select(ItemLinks).where(ItemLinks.Type == 'Season').limit(5)
        )
        print("\n修复后 Season 关联 (Type='Season'):")
        for link in result.scalars().all():
            print(f"  ItemId={link.ItemId} → LinkedItemId={link.LinkedItemId}, Type={link.Type}")

        result = await s.execute(
            select(ItemLinks).where(ItemLinks.Type == 'Episode').limit(5)
        )
        print("\n修复后 Episode 关联 (Type='Episode'):")
        for link in result.scalars().all():
            print(f"  ItemId={link.ItemId} → LinkedItemId={link.LinkedItemId}, Type={link.Type}")

    print("\n✅ 修复完成！")
    print("\n修复后的数据结构：")
    print("  Episode.ItemId → Season.LinkedItemId (Type='Episode')")
    print("  Season.ItemId → Series.LinkedItemId (Type='Season')")


if __name__ == '__main__':
    asyncio.run(fix_itemlinks_direction())