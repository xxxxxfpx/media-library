# coding: utf-8
"""
手动添加 FavoritedAt 字段到数据库
"""

import sqlite3

# 连接数据库
conn = sqlite3.connect('data/database/media.db')
cursor = conn.cursor()

# 添加 FavoritedAt 列
try:
    cursor.execute('ALTER TABLE UserData ADD COLUMN FavoritedAt DATETIME')
    print("✓ 成功添加 FavoritedAt 列")
except sqlite3.OperationalError as e:
    if "duplicate column" in str(e).lower():
        print("✓ FavoritedAt 列已存在")
    else:
        raise e

# 添加索引
try:
    cursor.execute('CREATE INDEX idx_user_data_favorited_at ON UserData(FavoritedAt)')
    print("✓ 成功创建 idx_user_data_favorited_at 索引")
except sqlite3.OperationalError as e:
    if "already exists" in str(e).lower():
        print("✓ 索引已存在")
    else:
        raise e

conn.commit()
conn.close()

print("✓ 数据库迁移完成！")
