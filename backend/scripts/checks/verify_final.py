"""验证修复后的查询逻辑"""
import os
import sqlite3

conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'database', 'media.db'))
cur = conn.cursor()

print("=" * 60)
print("验证修复后的查询逻辑")
print("=" * 60)

# 修复后的数据结构：
# - Episode.ItemId → Season.LinkedItemId (Type='Episode')
# - Season.ItemId → Series.LinkedItemId (Type='Season')

# 场景1：查询 Series 24747 的 Season
# 使用 linked_item_ids：WHERE LinkedItemId = 24747 AND Type = 'Season'
print("\n=== 场景1：查询 Series 24747 的 Season ===")
print("SQL: SELECT * FROM MediaItems WHERE Id IN (SELECT ItemId FROM ItemLinks WHERE LinkedItemId = 24747 AND Type = 'Season')")

cur.execute('''
    SELECT mi.Id, mi.Name, mi.Type
    FROM MediaItems mi
    WHERE mi.Id IN (
        SELECT ItemId FROM ItemLinks
        WHERE LinkedItemId = 24747 AND Type = 'Season'
    )
''')
results = cur.fetchall()
print(f"结果数: {len(results)}")
for r in results:
    print(f"  Id={r[0]}, Name={r[1][:40]}, Type={r[2]}")

# 场景2：查询 Season 24748 的 Episode
# 使用 linked_item_ids：WHERE LinkedItemId = 24748 AND Type = 'Episode'
print("\n=== 场景2：查询 Season 24748 的 Episode ===")
print("SQL: SELECT * FROM MediaItems WHERE Id IN (SELECT ItemId FROM ItemLinks WHERE LinkedItemId = 24748 AND Type = 'Episode')")

cur.execute('''
    SELECT mi.Id, mi.Name, mi.Type
    FROM MediaItems mi
    WHERE mi.Id IN (
        SELECT ItemId FROM ItemLinks
        WHERE LinkedItemId = 24748 AND Type = 'Episode'
    )
''')
results = cur.fetchall()
print(f"结果数: {len(results)}")
for r in results[:5]:
    print(f"  Id={r[0]}, Name={r[1][:40]}, Type={r[2]}")
if len(results) > 5:
    print(f"  ... 还有 {len(results) - 5} 条")

conn.close()
print("\n✅ 查询逻辑验证完成")
