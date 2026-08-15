import os
import sqlite3

conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'database', 'media.db'))
cursor = conn.cursor()

print('=== 表记录数 ===')
cursor.execute('SELECT COUNT(*) FROM MediaItems')
print(f'MediaItems: {cursor.fetchone()[0]}')
cursor.execute('SELECT COUNT(*) FROM ItemLinks')
print(f'ItemLinks: {cursor.fetchone()[0]}')
cursor.execute('SELECT COUNT(*) FROM Files')
print(f'Files: {cursor.fetchone()[0]}')

print()
print('=== 索引信息 ===')
cursor.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='index' AND tbl_name IN ('MediaItems', 'ItemLinks', 'Files')")
for row in cursor.fetchall():
    print(f'{row[0]} on {row[1]}')

print()
print('=== Episode 类型记录数 ===')
cursor.execute("SELECT COUNT(*) FROM MediaItems WHERE Type='Episode'")
print(f'Episode 数量: {cursor.fetchone()[0]}')

print()
print('=== 慢查询分析 ===')
cursor.execute("""
    SELECT COUNT(*)
    FROM ItemLinks
    WHERE LinkedItemId IN (SELECT Id FROM MediaItems WHERE Type='Episode' AND IsDeleted=0)
""")
print(f'ItemLinks 中关联到 Episode 的记录数: {cursor.fetchone()[0]}')

print()
print('=== EXPLAIN 查询计划 ===')
query = """
    SELECT ItemLinks.ItemId, MediaItems.Id, MediaItems.Name
    FROM ItemLinks
    JOIN MediaItems ON ItemLinks.LinkedItemId = MediaItems.Id
    WHERE ItemLinks.ItemId IN (24328, 24327, 24326, 24325, 24324) AND MediaItems.IsDeleted = 0
"""
cursor.execute(f"EXPLAIN QUERY PLAN {query}")
for row in cursor.fetchall():
    print(row)

conn.close()
