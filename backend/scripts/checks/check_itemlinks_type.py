"""检查 ItemLinks 表中 Type 字段的实际值"""
import os
import sqlite3

conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'database', 'media.db'))
cur = conn.cursor()

print("=" * 60)
print("检查 ItemLinks Type 字段的实际值")
print("=" * 60)

# 1. 查看 ItemLinks 表中有哪些 Type 值
print("\n=== ItemLinks 中所有的 Type 值 ===")
cur.execute('SELECT Type, COUNT(*) FROM ItemLinks GROUP BY Type ORDER BY COUNT(*) DESC')
for row in cur.fetchall():
    print(f"  Type='{row[0]}': {row[1]} 条")

# 2. 查看 ID=24747 的 Series 的所有关联
print("\n=== Series 24747 的所有关联 ===")
cur.execute('''
    SELECT il.Id, il.ItemId, il.LinkedItemId, il.Type, mi.Name, mi.Type as LinkedType
    FROM ItemLinks il
    JOIN MediaItems mi ON il.LinkedItemId = mi.Id
    WHERE il.ItemId = 24747
''')
links = cur.fetchall()
print(f"关联数量: {len(links)}")
for link in links:
    print(f"  Id={link[0]}, ItemId={link[1]}, LinkedItemId={link[2]}, Type='{link[3]}', LinkedName='{link[4][:30]}', LinkedType='{link[5]}'")

# 3. 对比：检查 MediaType.Season 的字符串值
print("\n=== 检查 MediaType.Season 的值 ===")
print("MediaType.Season = 'Season'")
print("所以 Type='Season' 表示关联到 Season 类型的 MediaItem")

# 4. 检查 Season 24748 的所有关联
print("\n=== Season 24748 的所有关联 ===")
cur.execute('''
    SELECT il.Id, il.ItemId, il.LinkedItemId, il.Type, mi.Name, mi.Type as LinkedType
    FROM ItemLinks il
    JOIN MediaItems mi ON il.LinkedItemId = mi.Id
    WHERE il.ItemId = 24748
''')
season_links = cur.fetchall()
print(f"关联数量: {len(season_links)}")
for link in season_links:
    print(f"  Id={link[0]}, ItemId={link[1]}, LinkedItemId={link[2]}, Type='{link[3]}', LinkedName='{link[4][:30]}', LinkedType='{link[5]}'")

# 5. 检查前端如何查询 Season
print("\n=== 检查前端查询逻辑 ===")
print("前端可能按 Type='Season' 查询，但关联的 Type 可能不是 'Season'")

conn.close()
