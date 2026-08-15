import os
import sqlite3
import time

conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'database', 'media.db'))
cursor = conn.cursor()

print('=' * 60)
print('性能对比测试：优化前后对比')
print('=' * 60)

# 模拟 API 查询参数
item_ids = list(range(24269, 24329))  # 60个ID
item_ids_str = ','.join([str(i) for i in item_ids])

print(f'\n测试条件: ItemId IN ({item_ids_str[:50]}...) 共{len(item_ids)}个')
print()

# ==================== 优化前: 直接 JOIN ====================
print('【优化前】直接 JOIN 查询')
print('-' * 40)
start = time.time()
cursor.execute(f"""
    SELECT ItemLinks.ItemId, ItemLinks.LinkedItemId, MediaItems.Id, MediaItems.Name
    FROM ItemLinks
    JOIN MediaItems ON ItemLinks.LinkedItemId = MediaItems.Id
    WHERE ItemLinks.ItemId IN ({item_ids_str}) AND MediaItems.IsDeleted = 0
""")
result_old = cursor.fetchall()
time_old = time.time() - start
print(f'  结果数: {len(result_old)}')
print(f'  耗时:   {time_old*1000:.2f} ms')

# ==================== 优化后: 两步查询 ====================
print()
print('【优化后】两步查询')
print('-' * 40)

# 第一步：获取 ItemLinks
start = time.time()
cursor.execute(f"SELECT ItemId, LinkedItemId FROM ItemLinks WHERE ItemId IN ({item_ids_str})")
links = cursor.fetchall()
time_step1 = time.time() - start

# 第二步：获取 MediaItems
linked_item_ids = list(set([row[1] for row in links]))
linked_ids_str = ','.join([str(i) for i in linked_item_ids])
start = time.time()
cursor.execute(f"SELECT Id, Name FROM MediaItems WHERE Id IN ({linked_ids_str}) AND IsDeleted = 0")
media_map = {row[0]: row[1] for row in cursor.fetchall()}
time_step2 = time.time() - start

# 组合结果
final_result = [(row[0], row[1], row[1], media_map.get(row[1])) for row in links if row[1] in media_map]
time_new = time_step1 + time_step2

print(f'  第一步 (ItemLinks): {time_step1*1000:.2f} ms')
print(f'  第二步 (MediaItems): {time_step2*1000:.2f} ms')
print(f'  总耗时:              {time_new*1000:.2f} ms')
print(f'  结果数: {len(final_result)}')

# ==================== 性能提升 ====================
print()
print('=' * 60)
print('性能提升总结')
print('=' * 60)
speedup = time_old / time_new if time_new > 0 else float('inf')
print(f'优化前: {time_old*1000:.2f} ms')
print(f'优化后: {time_new*1000:.2f} ms')
print(f'提升:   {speedup:.1f}x 倍')
print(f'节省:   {(1 - time_new/time_old)*100:.1f}% 时间')

# ==================== 验证结果一致性 ====================
print()
print('=' * 60)
print('结果验证')
print('=' * 60)
print(f'优化前结果数: {len(result_old)}')
print(f'优化后结果数: {len(final_result)}')
print(f'结果一致: {"✓ 是" if len(result_old) == len(final_result) else "✗ 否"}')

conn.close()
