"""检查 MediaItem ID=24747 及其 Season 关联"""
import os
import sqlite3

conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'database', 'media.db'))
cur = conn.cursor()

print("=" * 60)
print("检查 MediaItem ID=24747")
print("=" * 60)

# 1. 查看 MediaItem 24747 的基本信息
print("\n=== MediaItem 24747 信息 ===")
cur.execute('''
    SELECT Id, Type, Name
    FROM MediaItems
    WHERE Id = 24747
''')
row = cur.fetchone()
if row:
    print(f"ID: {row[0]}, Type: {row[1]}, Name: {row[2]}")
else:
    print("❌ MediaItem 24747 不存在")

# 2. 查看 24747 的 Season 关联
print("\n=== Series 24747 的 Season 关联 ===")
cur.execute('''
    SELECT il.LinkedItemId, mi.Name, mi.Type
    FROM ItemLinks il
    JOIN MediaItems mi ON il.LinkedItemId = mi.Id
    WHERE il.ItemId = 24747 AND il.Type = 'Season'
''')
seasons = cur.fetchall()
print(f"Season 数量: {len(seasons)}")
for s in seasons:
    print(f"  Season ID={s[0]}, Name={s[1]}")

# 3. 查看 24748 的详情
print("\n=== Season 24748 详情 ===")
cur.execute('SELECT Id, Type, Name FROM MediaItems WHERE Id = 24748')
season_row = cur.fetchone()
if season_row:
    print(f"ID: {season_row[0]}, Type: {season_row[1]}, Name: {season_row[2]}")
else:
    print("❌ Season 24748 不存在")

# 4. 查看 Season 24748 下的 Episode
print("\n=== Season 24748 的 Episode 关联 ===")
cur.execute('''
    SELECT il.LinkedItemId, mi.Name, mi.Type
    FROM ItemLinks il
    JOIN MediaItems mi ON il.LinkedItemId = mi.Id
    WHERE il.ItemId = 24748 AND il.Type = 'Episode'
''')
episodes = cur.fetchall()
print(f"Episode 数量: {len(episodes)}")
for ep in episodes:
    print(f"  Episode ID={ep[0]}, Name={ep[1]}")

conn.close()

print("\n" + "=" * 60)
print("总结:")
print("=" * 60)
print(f"24747 是 Series: {'是' if row and row[1] == 'Series' else '否'}")
print(f"24747 有 Season: {len(seasons) > 0}")
if seasons:
    print(f"  Season ID: {seasons[0][0]}")
    print(f"Season 24748 有 Episode: {len(episodes) > 0}")
    print(f"  Episode 数量: {len(episodes)}")
