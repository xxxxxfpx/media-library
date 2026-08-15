"""检查数据库中的CollectionFolder数据"""
import os
import sqlite3
conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'database', 'media.db'))
cur = conn.cursor()
cur.execute("SELECT Id, Name, Type FROM MediaItems WHERE Type='CollectionFolder'")
rows = cur.fetchall()
for row in rows:
    print(f"ID={row[0]}, Name={row[1]}, Type={row[2]}")
print(f"\n总计 {len(rows)} 个CollectionFolder")

cur.execute("SELECT Type, COUNT(*) FROM MediaItems GROUP BY Type ORDER BY Type")
rows = cur.fetchall()
for row in rows:
    print(f"Type={row[0]}, Count={row[1]}")

cur.execute("SELECT COUNT(*) FROM MediaItems")
total = cur.fetchone()[0]
print(f"\nMediaItems总数: {total}")
conn.close()
