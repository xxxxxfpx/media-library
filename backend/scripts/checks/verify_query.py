import os
import sqlite3

conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'database', 'media.db'))
cursor = conn.cursor()

print('=== 验证查询: linked_item_ids=1, types=Episode ===')
print()

print('Step 1: 子查询 - 找出所有关联到 ID=1 的 ItemId')
cursor.execute("""
    SELECT ItemId, LinkedItemId
    FROM ItemLinks
    WHERE LinkedItemId = 1
""")
rows = cursor.fetchall()
print(f'结果数: {len(rows)}')
for row in rows[:10]:
    print(f'  ItemId={row[0]}, LinkedItemId={row[1]}')

print()
print('Step 2: 主查询 - 找出这些 ItemId 中 Type=Episode 的 MediaItem')
cursor.execute("""
    SELECT Id, Type, Name, DateCreated
    FROM MediaItems
    WHERE Id IN (SELECT ItemId FROM ItemLinks WHERE LinkedItemId = 1)
    AND Type = 'Episode'
    ORDER BY DateCreated DESC
""")
rows = cursor.fetchall()
print(f'Episode 总数: {len(rows)}')
for row in rows[:10]:
    print(f'  ID={row[0]}, Type={row[1]}, Name={row[2]}')

print()
print('Step 3: 带 OFFSET/LIMIT 的查询 (offset=360, limit=60)')
cursor.execute("""
    SELECT Id, Type, Name, DateCreated
    FROM MediaItems
    WHERE Id IN (SELECT ItemId FROM ItemLinks WHERE LinkedItemId = 1)
    AND Type = 'Episode'
    ORDER BY DateCreated DESC
    LIMIT 60 OFFSET 360
""")
rows = cursor.fetchall()
print(f'结果数: {len(rows)}')
for row in rows:
    print(f'  ID={row[0]}, Type={row[1]}, Name={row[2]}')

print()
print('=== 性能测试 ===')
import time

# 测试子查询性能
start = time.time()
cursor.execute("""
    SELECT ItemId FROM ItemLinks WHERE LinkedItemId = 1
""")
subq_result = cursor.fetchall()
subq_time = time.time() - start
print(f'子查询时间: {subq_time*1000:.2f}ms, 结果数: {len(subq_result)}')

# 测试主查询性能
start = time.time()
cursor.execute("""
    SELECT Id, Type, Name
    FROM MediaItems
    WHERE Id IN (SELECT ItemId FROM ItemLinks WHERE LinkedItemId = 1)
    AND Type = 'Episode'
    ORDER BY DateCreated DESC
    LIMIT 60 OFFSET 360
""")
main_result = cursor.fetchall()
main_time = time.time() - start
print(f'主查询时间: {main_time*1000:.2f}ms, 结果数: {len(main_result)}')

print()
print('=== 检查实际 IN 子句参数 ===')
cursor.execute("SELECT Id FROM MediaItems WHERE Id IN (SELECT ItemId FROM ItemLinks WHERE LinkedItemId = 1) AND Type = 'Episode' ORDER BY DateCreated DESC LIMIT 60 OFFSET 360")
print(f'实际返回的 ItemId 数量: {len(cursor.fetchall())}')

conn.close()
