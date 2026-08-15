# coding: utf-8
"""
删除 Likes 字段
"""

import sqlite3

# 连接数据库
conn = sqlite3.connect('data/database/media.db')
cursor = conn.cursor()

# 删除 Likes 列
try:
    cursor.execute('ALTER TABLE UserData DROP COLUMN Likes')
    print("✓ 成功删除 Likes 列")
except sqlite3.OperationalError as e:
    if "no such column" in str(e).lower():
        print("✓ Likes 列已不存在")
    else:
        raise e

conn.commit()
conn.close()

print("✓ 数据库迁移完成！")
