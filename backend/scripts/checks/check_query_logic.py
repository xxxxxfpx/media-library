"""检查后端 linked_item_ids 查询逻辑"""
import os
import sqlite3

conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'database', 'media.db'))
cur = conn.cursor()

print("=" * 60)
print("验证后端 linked_item_ids 查询逻辑")
print("=" * 60)

# 模拟后端查询逻辑
# subq = select(ItemLinks.ItemId).where(ItemLinks.LinkedItemId.in_(linked_ids))
# query = query.where(MediaItem.Id.in_(subq))

print("\n=== 错误查询逻辑 (LinkedItemId = 24747) ===")
cur.execute('''
    SELECT DISTINCT il.ItemId, mi.Name, mi.Type
    FROM ItemLinks il
    JOIN MediaItems mi ON il.ItemId = mi.Id
    WHERE il.LinkedItemId = 24747
''')
wrong_results = cur.fetchall()
print(f"结果数: {len(wrong_results)}")
for r in wrong_results[:5]:
    print(f"  ItemId={r[0]}, Name={r[1][:30]}, Type={r[2]}")

print("\n=== 正确查询逻辑 (ItemId = 24747 AND Type = 'Season') ===")
cur.execute('''
    SELECT il.LinkedItemId, mi.Name, mi.Type
    FROM ItemLinks il
    JOIN MediaItems mi ON il.LinkedItemId = mi.Id
    WHERE il.ItemId = 24747 AND il.Type = 'Season'
''')
correct_results = cur.fetchall()
print(f"结果数: {len(correct_results)}")
for r in correct_results:
    print(f"  LinkedItemId={r[0]}, Name={r[1][:30]}, Type={r[2]}")

print("\n=== 正确的查询用 MediaItem.Type 筛选 ===")
cur.execute('''
    SELECT mi.Id, mi.Name, mi.Type
    FROM MediaItems mi
    WHERE mi.Id IN (
        SELECT LinkedItemId FROM ItemLinks WHERE ItemId = 24747 AND Type = 'Season'
    )
    AND mi.Type = 'Season'
''')
final_results = cur.fetchall()
print(f"结果数: {len(final_results)}")
for r in final_results:
    print(f"  Id={r[0]}, Name={r[1][:30]}, Type={r[2]}")

conn.close()
