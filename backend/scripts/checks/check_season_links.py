"""检查 Season 关联的详细类型"""
import os
import sqlite3

conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'database', 'media.db'))
cur = conn.cursor()

print("=" * 60)
print("检查 Season 关联的详细类型")
print("=" * 60)

# 检查所有 Type='Season' 的关联的详细信息
print("\n=== 所有 Season 关联的详细信息 ===")
cur.execute('''
    SELECT il.ItemId, il.LinkedItemId, il.Type,
           mi1.Name as ItemName, mi1.Type as ItemType,
           mi2.Name as LinkedName, mi2.Type as LinkedType
    FROM ItemLinks il
    JOIN MediaItems mi1 ON il.ItemId = mi1.Id
    JOIN MediaItems mi2 ON il.LinkedItemId = mi2.Id
    WHERE il.Type = 'Season'
    LIMIT 20
''')
rows = cur.fetchall()
print(f"总共有 {len(rows)} 条 Type='Season' 的关联")

for row in rows[:10]:
    print(f"  ItemId={row[0]}({row[3][:20]},{row[4]}) -> LinkedItemId={row[1]}({row[5][:20]},{row[6]}), Type='{row[2]}'")

# 检查是否有不是指向 Series 的 Season 关联
print("\n=== Season 关联指向 Series 的情况 ===")
cur.execute('''
    SELECT COUNT(*)
    FROM ItemLinks il
    JOIN MediaItems mi2 ON il.LinkedItemId = mi2.Id
    WHERE il.Type = 'Season' AND mi2.Type = 'Series'
''')
count = cur.fetchone()[0]
print(f"Type='Season' 且指向 Series: {count} 条")

# 检查 Type='Season' 且指向非 Series 的情况
print("\n=== Season 关联不指向 Series 的情况 ===")
cur.execute('''
    SELECT il.ItemId, il.LinkedItemId, mi2.Type as LinkedType
    FROM ItemLinks il
    JOIN MediaItems mi2 ON il.LinkedItemId = mi2.Id
    WHERE il.Type = 'Season' AND mi2.Type != 'Series'
    LIMIT 10
''')
non_series = cur.fetchall()
print(f"Type='Season' 但不指向 Series: {len(non_series)} 条")
for row in non_series:
    print(f"  ItemId={row[0]}, LinkedItemId={row[1]}, LinkedType={row[2]}")

conn.close()
