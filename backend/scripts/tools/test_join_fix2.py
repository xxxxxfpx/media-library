import os
import sqlite3
import time

conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'database', 'media.db'))
cursor = conn.cursor()

print('=== 深入分析 JOIN 性能问题 ===')
print()

item_ids = tuple(range(24269, 24329))  # 60个ID

print('=== 测试 1: 直接 JOIN (慢) ===')
start = time.time()
cursor.execute(f"""
    SELECT ItemLinks.ItemId, ItemLinks.LinkedItemId, MediaItems.Id, MediaItems.Name
    FROM ItemLinks
    JOIN MediaItems ON ItemLinks.LinkedItemId = MediaItems.Id
    WHERE ItemLinks.ItemId IN {item_ids} AND MediaItems.IsDeleted = 0
""")
result = cursor.fetchall()
elapsed = time.time() - start
print(f'直接 JOIN: {elapsed*1000:.2f}ms, 结果数: {len(result)}')

print()
print('=== 测试 2: 使用子查询 ===')
start = time.time()
cursor.execute(f"""
    SELECT il.ItemId, il.LinkedItemId, m.Id, m.Name
    FROM (SELECT ItemId, LinkedItemId FROM ItemLinks WHERE ItemId IN {item_ids}) AS il
    JOIN MediaItems m ON il.LinkedItemId = m.Id
    WHERE m.IsDeleted = 0
""")
result = cursor.fetchall()
elapsed = time.time() - start
print(f'子查询方式: {elapsed*1000:.2f}ms, 结果数: {len(result)}')

print()
print('=== 验证执行计划 ===')
print('直接 JOIN:')
cursor.execute(f"""
    EXPLAIN QUERY PLAN
    SELECT ItemLinks.ItemId, ItemLinks.LinkedItemId
    FROM ItemLinks
    JOIN MediaItems ON ItemLinks.LinkedItemId = MediaItems.Id
    WHERE ItemLinks.ItemId IN {item_ids} AND MediaItems.IsDeleted = 0
""")
for row in cursor.fetchall():
    print(f'  {row}')

conn.close()
