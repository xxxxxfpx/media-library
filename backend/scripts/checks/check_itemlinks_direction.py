"""检查 ItemLinks 的关联方向"""
import os
import sqlite3

conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'database', 'media.db'))
cur = conn.cursor()

print("=" * 60)
print("检查 ItemLinks 的关联方向")
print("=" * 60)

# 检查 Season 24748 的所有关联（它作为 ItemId）
print("\n=== Season 24748 的关联 (ItemId=24748) ===")
cur.execute('''
    SELECT il.ItemId, il.LinkedItemId, il.Type, mi.Name, mi.Type as LinkedType
    FROM ItemLinks il
    JOIN MediaItems mi ON il.LinkedItemId = mi.Id
    WHERE il.ItemId = 24748
''')
season_links = cur.fetchall()
for link in season_links:
    print(f"  ItemId={link[0]}({link[3][:20]}) -> LinkedItemId={link[1]}({link[4]}), Type='{link[2]}'")

# 检查 Episode 24591 的关联（它作为 ItemId）
print("\n=== Episode 24591 的关联 (ItemId=24591) ===")
cur.execute('''
    SELECT il.ItemId, il.LinkedItemId, il.Type, mi.Name, mi.Type as LinkedType
    FROM ItemLinks il
    JOIN MediaItems mi ON il.LinkedItemId = mi.Id
    WHERE il.ItemId = 24591
''')
episode_links = cur.fetchall()
for link in episode_links:
    print(f"  ItemId={link[0]}({link[3][:20]}) -> LinkedItemId={link[1]}({link[4]}), Type='{link[2]}'")

# 检查反向查找：谁关联到了 Season 24748
print("\n=== 谁关联到了 Season 24748 (LinkedItemId=24748) ===")
cur.execute('''
    SELECT il.ItemId, il.LinkedItemId, il.Type, mi.Name, mi.Type
    FROM ItemLinks il
    JOIN MediaItems mi ON il.ItemId = mi.Id
    WHERE il.LinkedItemId = 24748
''')
reverse_season = cur.fetchall()
for link in reverse_season:
    print(f"  ItemId={link[0]}({link[3][:20]}) -> LinkedItemId={link[1]}, Type='{link[2]}'")

# 检查反向查找：谁关联到了 Episode 24591
print("\n=== 谁关联到了 Episode 24591 (LinkedItemId=24591) ===")
cur.execute('''
    SELECT il.ItemId, il.LinkedItemId, il.Type, mi.Name, mi.Type
    FROM ItemLinks il
    JOIN MediaItems mi ON il.ItemId = mi.Id
    WHERE il.LinkedItemId = 24591
''')
reverse_episode = cur.fetchall()
for link in reverse_episode:
    print(f"  ItemId={link[0]}({link[3][:20]}) -> LinkedItemId={link[1]}, Type='{link[2]}'")

print("\n" + "=" * 60)
print("正确的数据结构应该是：")
print("  - Episode.ItemId -> Season.LinkedItemId (Type='Episode')")
print("  - Season.ItemId -> Series.LinkedItemId (Type='Season')")
print("=" * 60)

conn.close()
