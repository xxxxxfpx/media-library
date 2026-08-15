import os
import sqlite3

conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'database', 'media.db'))
cursor = conn.cursor()

print('=== 分析 linked_item_ids=1 的关联关系 ===')
cursor.execute("""
    SELECT il.ItemId, il.LinkedItemId, mi.Type, mi.Name
    FROM ItemLinks il
    JOIN MediaItems mi ON il.ItemId = mi.Id
    WHERE il.LinkedItemId = 1 AND mi.Type = 'Episode'
    LIMIT 10
""")
rows = cursor.fetchall()
print(f'直接关联到 ID=1 的 Episode 数量: {len(rows)}')
for row in rows[:5]:
    print(f'  ItemId={row[0]}, LinkedItemId={row[1]}, Type={row[2]}, Name={row[3]}')

print()
print('=== 分析 Episode 的层级关系 ===')
cursor.execute("""
    SELECT il.ItemId, mi.Type, mi.Name, il2.LinkedItemId, mi2.Type as ParentType
    FROM ItemLinks il
    JOIN MediaItems mi ON il.ItemId = mi.Id
    LEFT JOIN ItemLinks il2 ON il2.ItemId = mi.Id
    LEFT JOIN MediaItems mi2 ON il2.LinkedItemId = mi2.Id
    WHERE mi.Type = 'Episode'
    LIMIT 10
""")
rows = cursor.fetchall()
print('Episode 及其关联的父级:')
for row in rows[:5]:
    print(f'  Episode ID={row[0]}, Name={row[2]}, Parent LinkedItemId={row[3]}, ParentType={row[4]}')

print()
print('=== 查看 ID=1 是什么类型的 MediaItem ===')
cursor.execute("SELECT Id, Type, Name FROM MediaItems WHERE Id = 1")
row = cursor.fetchone()
print(f'ID=1: Type={row[1]}, Name={row[2]}')

print()
print('=== 查看 ID=1 的关联项 ===')
cursor.execute("""
    SELECT il.LinkedItemId, mi.Type, mi.Name
    FROM ItemLinks il
    JOIN MediaItems mi ON il.LinkedItemId = mi.Id
    WHERE il.ItemId = 1
    LIMIT 20
""")
rows = cursor.fetchall()
print(f'ID=1 关联到的项目数: {len(rows)}')
for row in rows[:10]:
    print(f'  LinkedItemId={row[0]}, Type={row[1]}, Name={row[2]}')

print()
print('=== 实际执行的慢查询分析 ===')
cursor.execute("""
    SELECT il.ItemId, COUNT(*) as cnt
    FROM ItemLinks il
    WHERE il.LinkedItemId IN (SELECT Id FROM MediaItems WHERE Type='Episode')
    GROUP BY il.ItemId
    ORDER BY cnt DESC
    LIMIT 10
""")
rows = cursor.fetchall()
print('关联到 Episode 的 ItemId 统计:')
for row in rows:
    print(f'  ItemId={row[0]}, 关联Episode数={row[1]}')

print()
print('=== 测试实际慢查询的查询计划 ===')
print('查询: SELECT ... FROM ItemLinks WHERE ItemId IN (SELECT ItemId FROM ItemLinks WHERE LinkedItemId=1)')
query = """
    EXPLAIN QUERY PLAN
    SELECT DISTINCT il.ItemId
    FROM ItemLinks il
    WHERE il.ItemId IN (SELECT ItemId FROM ItemLinks WHERE LinkedItemId = 1)
"""
cursor.execute(query)
for row in cursor.fetchall():
    print(row)

conn.close()
