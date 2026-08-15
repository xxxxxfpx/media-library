import os
import sqlite3
import time

conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'database', 'media.db'))
cursor = conn.cursor()

print('=== 深入分析 JOIN 性能问题 ===')
print()

# 测试不同的查询方式
item_ids = tuple(range(24269, 24329))  # 60个ID

print('=== 测试 1: 直接 JOIN (慢) ===')
start = time.time()
cursor.execute(f"""
    SELECT il.ItemId, il.LinkedItemId, MediaItems.Id, MediaItems.Name
    FROM ItemLinks
    JOIN MediaItems ON ItemLinks.LinkedItemId = MediaItems.Id
    WHERE ItemLinks.ItemId IN {item_ids} AND MediaItems.IsDeleted = 0
""")
result = cursor.fetchall()
elapsed = time.time() - start
print(f'直接 JOIN: {elapsed*1000:.2f}ms, 结果数: {len(result)}')

print()
print('=== 测试 2: 使用子查询代替 JOIN ===')
start = time.time()
cursor.execute(f"""
    SELECT MediaItems.ItemId, MediaItems.LinkedItemId, MediaItems.Id, MediaItems.Name
    FROM (
        SELECT ItemId, LinkedItemId FROM ItemLinks WHERE ItemId IN {item_ids}
    ) AS MediaItems
    JOIN MediaItems ON MediaItems.LinkedItemId = MediaItems.Id
    WHERE MediaItems.IsDeleted = 0
""")
result = cursor.fetchall()
elapsed = time.time() - start
print(f'子查询: {elapsed*1000:.2f}ms, 结果数: {len(result)}')

print()
print('=== 测试 3: 分步执行 (最快) ===')
start = time.time()
# 第一步：获取 ItemId IN 条件的结果
cursor.execute(f"SELECT ItemId, LinkedItemId FROM ItemLinks WHERE ItemId IN {item_ids}")
links = {row[0]: row[1] for row in cursor.fetchall()}

# 第二步：获取 LinkedItemId
linked_ids = list(set(links.values()))
placeholders = ','.join(['?' for _ in linked_ids])

# 第三步：获取 MediaItems
cursor.execute(f"SELECT Id, Name FROM MediaItems WHERE Id IN ({placeholders}) AND IsDeleted = 0", linked_ids)
media = {row[0]: row[1] for row in cursor.fetchall()}

# 第四步：组合结果
result = [(item_id, linked_id, linked_id, media.get(linked_id, '')) for item_id, linked_id in links.items() if linked_id in media]
elapsed = time.time() - start
print(f'分步执行: {elapsed*1000:.2f}ms, 结果数: {len(result)}')

print()
print('=== 验证执行计划 ===')
print('直接 JOIN 的执行计划:')
cursor.execute(f"""
    EXPLAIN QUERY PLAN
    SELECT il.ItemId, il.LinkedItemId
    FROM ItemLinks il
    JOIN MediaItems ON il.LinkedItemId = MediaItems.Id
    WHERE il.ItemId IN {item_ids} AND MediaItems.IsDeleted = 0
""")
for row in cursor.fetchall():
    print(f'  {row}')

print()
print('不带 IsDeleted 条件的执行计划:')
cursor.execute(f"""
    EXPLAIN QUERY PLAN
    SELECT il.ItemId, il.LinkedItemId
    FROM ItemLinks il
    JOIN MediaItems ON il.LinkedItemId = MediaItems.Id
    WHERE il.ItemId IN {item_ids}
""")
for row in cursor.fetchall():
    print(f'  {row}')

conn.close()
