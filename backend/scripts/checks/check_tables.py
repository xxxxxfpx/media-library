"""检查数据库实际表名和 Alias 模型"""
import os
import sqlite3

conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'database', 'media.db'))
cur = conn.cursor()

print("=" * 60)
print("检查数据库实际表名")
print("=" * 60)

# 检查所有表
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cur.fetchall()
print("\n数据库中的表:")
for t in tables:
    print(f"  {t[0]}")

# 检查 Aliases 表结构
print("\n=== Aliases 表结构 ===")
try:
    cur.execute("PRAGMA table_info(Aliases)")
    columns = cur.fetchall()
    for col in columns:
        print(f"  {col[1]}: {col[2]}")
except sqlite3.OperationalError as e:
    print(f"  错误: {e}")

# 检查 MediaItems 表结构
print("\n=== MediaItems 表结构 ===")
cur.execute("PRAGMA table_info(MediaItems)")
columns = cur.fetchall()
for col in columns:
    print(f"  {col[1]}: {col[2]}")

conn.close()
