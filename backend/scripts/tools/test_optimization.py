import os
import sqlite3
import time

conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'database', 'media.db'))
cursor = conn.cursor()

print('=== 优化方案测试 ===')
print()

item_ids = tuple(range(24269, 24329))  # 60个ID

print('=== 原查询 (直接 JOIN) ===')
start = time.time()
cursor.execute(f"""
    SELECT ItemLinks.ItemId, ItemLinks.LinkedItemId, MediaItems.Id, MediaItems.Name
    FROM ItemLinks
    JOIN MediaItems ON ItemLinks.LinkedItemId = MediaItems.Id
    WHERE ItemLinks.ItemId IN {item_ids} AND MediaItems.IsDeleted = 0
""")
result = cursor.fetchall()
elapsed = time.time() - start
print(f'耗时: {elapsed*1000:.2f}ms, 结果数: {len(result)}')

print()
print('=== 优化方案: 子查询过滤 ItemLinks ===')
start = time.time()
cursor.execute(f"""
    SELECT il.ItemId, il.LinkedItemId, m.Id, m.Name
    FROM (
        SELECT ItemId, LinkedItemId FROM ItemLinks WHERE ItemId IN {item_ids}
    ) AS il
    JOIN MediaItems m ON il.LinkedItemId = m.Id
    WHERE m.IsDeleted = 0
""")
result = cursor.fetchall()
elapsed = time.time() - start
print(f'耗时: {elapsed*1000:.2f}ms, 结果数: {len(result)}')

print()
print('=== 优化方案: 两步查询 ===')
start = time.time()
# 第一步：获取 ItemLinks 结果
cursor.execute(f"SELECT ItemId, LinkedItemId FROM ItemLinks WHERE ItemId IN {item_ids}")
links = cursor.fetchall()
# 第二步：获取 MediaItems 结果
linked_ids = list(set([row[1] for row in links]))
placeholders = ','.join(['?' for _ in linked_ids])
cursor.execute(f"SELECT Id, Name FROM MediaItems WHERE Id IN ({placeholders}) AND IsDeleted = 0", linked_ids)
media_map = {row[0]: row[1] for row in cursor.fetchall()}
# 组合结果
final_result = [(row[0], row[1], row[1], media_map.get(row[1])) for row in links if row[1] in media_map]
elapsed = time.time() - start
print(f'耗时: {elapsed*1000:.2f}ms, 结果数: {len(final_result)}')

print()
print('=== 执行计划对比 ===')
print('原查询:')
cursor.execute(f"""
    EXPLAIN QUERY PLAN
    SELECT ItemLinks.ItemId, ItemLinks.LinkedItemId
    FROM ItemLinks
    JOIN MediaItems ON ItemLinks.LinkedItemId = MediaItems.Id
    WHERE ItemLinks.ItemId IN {item_ids} AND MediaItems.IsDeleted = 0
""")
for row in cursor.fetchall():
    print(f'  {row}')

print('子查询方案:')
cursor.execute(f"""
    EXPLAIN QUERY PLAN
    SELECT il.ItemId, il.LinkedItemId
    FROM (SELECT ItemId, LinkedItemId FROM ItemLinks WHERE ItemId IN {item_ids}) AS il
    JOIN MediaItems ON il.LinkedItemId = MediaItems.Id
    WHERE MediaItems.IsDeleted = 0
""")
for row in cursor.fetchall():
    print(f'  {row}')

conn.close()
