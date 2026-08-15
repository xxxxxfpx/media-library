"""检查数据库状态"""
import os
import sqlite3

conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'database', 'media.db'))
cur = conn.cursor()

print("=" * 60)
print("数据库状态检查")
print("=" * 60)

# 1. 检查 Files 表
print("\n=== Files 表 ===")
cur.execute("SELECT COUNT(*) FROM Files")
total_files = cur.fetchone()[0]
print(f"总文件数: {total_files}")

cur.execute("SELECT COUNT(*) FROM Files WHERE FFmpeg IS NOT NULL AND FFmpeg != ''")
has_ffmpeg = cur.fetchone()[0]
print(f"有 FFmpeg 数据的文件数: {has_ffmpeg}")

cur.execute("SELECT COUNT(*) FROM Files WHERE Type = 'Video'")
video_count = cur.fetchone()[0]
print(f"Video 类型文件数: {video_count}")

# 2. 检查 Aliases 表（复数）
print("\n=== Aliases 表（正确表名）===")
try:
    cur.execute("SELECT COUNT(*) FROM Aliases")
    alias_total = cur.fetchone()[0]
    print(f"Aliases 总数: {alias_total}")

    cur.execute("SELECT Source, COUNT(*) FROM Aliases GROUP BY Source")
    for row in cur.fetchall():
        print(f"  Source='{row[0]}': {row[1]} 条")
except sqlite3.OperationalError as e:
    print(f"❌ Aliases 表错误: {e}")

# 3. 检查 MediaItems 表
print("\n=== MediaItems 表 ===")
cur.execute("SELECT COUNT(*) FROM MediaItems")
mi_total = cur.fetchone()[0]
print(f"MediaItems 总数: {mi_total}")

cur.execute("SELECT Type, COUNT(*) FROM MediaItems GROUP BY Type ORDER BY Type")
for row in cur.fetchall():
    print(f"  Type={row[0]}: {row[1]}")

conn.close()
print("\n✅ 检查完成")
