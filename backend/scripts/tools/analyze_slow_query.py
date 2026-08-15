import os
import sqlite3
import time

conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'database', 'media.db'))
cursor = conn.cursor()

print('=== 深入分析慢查询 ===')
print()

# 模拟日志中的 ItemLinks JOIN 查询
item_ids = tuple(range(24269, 24329))  # 60个ID
print(f'查询条件: ItemId IN {item_ids[:5]}... (共{len(item_ids)}个)')

print()
print('=== 测试 1: ItemLinks 查询 ===')
start = time.time()
cursor.execute(f"""
    SELECT ItemLinks.ItemId, ItemLinks.LinkedItemId, MediaItems.Type, MediaItems.Name
    FROM ItemLinks
    JOIN MediaItems ON ItemLinks.LinkedItemId = MediaItems.Id
    WHERE ItemLinks.ItemId IN {item_ids} AND MediaItems.IsDeleted = 0
""")
result = cursor.fetchall()
elapsed = time.time() - start
print(f'结果数: {len(result)}')
print(f'耗时: {elapsed*1000:.2f}ms')

print()
print('=== 测试 2: 单独测试 ItemLinks.ItemId IN 查询 ===')
start = time.time()
cursor.execute(f"""
    SELECT COUNT(*) FROM ItemLinks WHERE ItemId IN {item_ids}
""")
result = cursor.fetchone()
elapsed = time.time() - start
print(f'ItemLinks 记录数: {result[0]}')
print(f'耗时: {elapsed*1000:.2f}ms')

print()
print('=== 测试 3: 逐步测试 JOIN ===')
start = time.time()
cursor.execute(f"""
    SELECT il.ItemId, il.LinkedItemId
    FROM ItemLinks il
    WHERE il.ItemId IN {item_ids}
""")
links = cursor.fetchall()
print(f'ItemLinks 查询耗时: {(time.time()-start)*1000:.2f}ms, 结果数: {len(links)}')

linked_ids = tuple(set([r[1] for r in links]))
print(f'唯一 LinkedItemId 数: {len(linked_ids)}')

start = time.time()
cursor.execute(f"""
    SELECT Id, Type, Name
    FROM MediaItems
    WHERE Id IN {linked_ids} AND IsDeleted = 0
""")
media = cursor.fetchall()
print(f'MediaItems 查询耗时: {(time.time()-start)*1000:.2f}ms, 结果数: {len(media)}')

print()
print('=== 检查索引使用情况 ===')
print('当前 ItemLinks 索引:')
cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='ItemLinks'")
for row in cursor.fetchall():
    print(f'  {row[0]}')

print()
print('检查是否能创建更好的索引...')
# 建议的复合索引
print('建议: CREATE INDEX IF NOT EXISTS idx_item_links_itemid_linked ON ItemLinks(ItemId, LinkedItemId)')

print()
print('=== 测试带 IN 子句的查询计划 ===')
cursor.execute(f"EXPLAIN QUERY PLAN SELECT * FROM ItemLinks WHERE ItemId IN {item_ids[:5]}")
for row in cursor.fetchall():
    print(row)

conn.close()
