"""视频化精简前置检查

在运行 video_only_schema 迁移前执行：
- 统计 MediaItems 各类型数据量（确认无非视频类型数据）
- 统计 Files 各类型数据量
- 检查 MediaItems 是否仍存在 AlbumId 列（存在则迁移会删除）

用法（在 backend 目录）：
    python scripts/checks/check_video_only_prep.py
    # 或指定库文件：
    python scripts/checks/check_video_only_prep.py path/to/media.db
"""
import os
import sqlite3
import sys


def main() -> int:
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
    else:
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "database", "media.db")

    if not os.path.exists(db_path):
        print(f"[错误] 数据库不存在: {db_path}")
        return 1

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    print("=" * 60)
    print(f"检查库: {db_path}")
    print("=" * 60)

    print("\n=== MediaItems 类型分布 ===")
    try:
        rows = cur.execute("SELECT Type, COUNT(*) FROM MediaItems GROUP BY Type ORDER BY 2 DESC").fetchall()
        for t, c in rows:
            print(f"  {t}: {c}")
        print(f"  合计: {sum(c for _, c in rows)}")
    except sqlite3.OperationalError as e:
        print(f"  [错误] {e}")

    print("\n=== Files 类型分布 ===")
    try:
        rows = cur.execute("SELECT Type, COUNT(*) FROM Files GROUP BY Type").fetchall()
        for t, c in rows:
            print(f"  {t}: {c}")
        print(f"  合计: {sum(c for _, c in rows)}")
    except sqlite3.OperationalError as e:
        print(f"  [错误] {e}")

    print("\n=== 非视频类型数据检查 ===")
    video_types = {"Movie", "Series", "Season", "Episode", "BoxSet", "Genre",
                   "Person", "Studio", "Tag", "Folder", "Source", "Video",
                   "UserRootFolder", "UserView", "AggregateFolder", "Playlist"}
    non_video = []
    try:
        for t, c in cur.execute("SELECT Type, COUNT(*) FROM MediaItems GROUP BY Type"):
            if t not in video_types and c > 0:
                non_video.append((t, c))
    except sqlite3.OperationalError as e:
        print(f"  [错误] {e}")

    if non_video:
        print("  [警告] 发现非视频类型数据（迁移删除 AlbumId 不影响这些行，但请确认精简枚举后应用可正常读取）：")
        for t, c in non_video:
            print(f"    - {t}: {c}")
    else:
        print("  [OK] 未发现非视频类型数据")

    print("\n=== MediaItems 是否含 AlbumId 列 ===")
    try:
        cols = cur.execute("PRAGMA table_info(MediaItems)").fetchall()
        has_album = any(c[1] == "AlbumId" for c in cols)
        has_prod_year = any(c[1] == "ProductionYear" for c in cols)
        print(f"  AlbumId: {'存在（迁移将删除）' if has_album else '不存在'}")
        print(f"  ProductionYear: {'存在' if has_prod_year else '不存在'}")
    except sqlite3.OperationalError as e:
        print(f"  [错误] {e}")

    con.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
