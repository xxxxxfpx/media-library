"""
重建 ItemLinks 表，移除 Type 列
SQLite 不支持 DROP COLUMN，通过重建表的方式迁移
"""
import sqlite3
import os
import shutil
from datetime import datetime


DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'database', 'media.db')
BACKUP_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'database', 'media.db')


def migrate():
    print("=" * 60)
    print("重建 ItemLinks 表，移除 Type 列")
    print("=" * 60)

    # 1. 备份数据库
    print("\n1. 备份数据库...")
    if os.path.exists(DB_PATH):
        shutil.copy2(DB_PATH, BACKUP_PATH)
        print(f"   备份完成: {BACKUP_PATH}")
    else:
        print("   数据库文件不存在!")

    # 2. 连接数据库
    print("\n2. 连接数据库...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 3. 检查当前表结构
    print("\n3. 检查当前表结构...")
    cursor.execute("PRAGMA table_info(ItemLinks)")
    columns = cursor.fetchall()
    print("   当前列:")
    for col in columns:
        print(f"     {col[1]}: {col[2]}")

    # 4. 创建新表（无 Type 列）
    print("\n4. 创建新表 ItemLinks_new...")
    cursor.execute("""
        CREATE TABLE ItemLinks_new (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            ItemId INTEGER NOT NULL,
            LinkedItemId INTEGER NOT NULL,
            PeopleType TEXT,
            PeopleRole TEXT,
            CreatedAt TEXT NOT NULL,
            UpdatedAt TEXT NOT NULL,
            FOREIGN KEY (ItemId) REFERENCES MediaItems(Id) ON DELETE CASCADE,
            FOREIGN KEY (LinkedItemId) REFERENCES MediaItems(Id) ON DELETE CASCADE
        )
    """)
    print("   新表创建完成")

    # 5. 复制数据（SourceId/SourceLink 已迁移至 MediaItems 表）
    print("\n5. 复制数据到新表...")
    cursor.execute("SELECT COUNT(*) FROM ItemLinks")
    total = cursor.fetchone()[0]
    print(f"   总记录数: {total}")

    cursor.execute("""
        INSERT INTO ItemLinks_new (Id, ItemId, LinkedItemId, PeopleType, PeopleRole, CreatedAt, UpdatedAt)
        SELECT Id, ItemId, LinkedItemId, PeopleType, PeopleRole, CreatedAt, UpdatedAt
        FROM ItemLinks
    """)
    conn.commit()
    print("   数据复制完成")

    # 6. 删除旧表
    print("\n6. 删除旧表...")
    cursor.execute("DROP TABLE ItemLinks")
    print("   旧表已删除")

    # 7. 重命名新表
    print("\n7. 重命名新表...")
    cursor.execute("ALTER TABLE ItemLinks_new RENAME TO ItemLinks")
    print("   重命名完成")

    # 8. 重建索引
    print("\n8. 重建索引...")
    cursor.execute("CREATE INDEX idx_item_links_item_id ON ItemLinks(ItemId)")
    cursor.execute("CREATE INDEX idx_item_links_linked_item_id ON ItemLinks(LinkedItemId)")
    cursor.execute("CREATE INDEX idx_item_links_people_type ON ItemLinks(PeopleType)")
    print("   索引创建完成")

    # 9. 验证
    print("\n9. 验证新表结构...")
    cursor.execute("PRAGMA table_info(ItemLinks)")
    new_columns = cursor.fetchall()
    print("   新列:")
    for col in new_columns:
        print(f"     {col[1]}: {col[2]}")

    cursor.execute("SELECT COUNT(*) FROM ItemLinks")
    new_count = cursor.fetchone()[0]
    print(f"   新记录数: {new_count}")

    conn.close()
    print("\n✅ 迁移完成!")
    print(f"\n原始数据库已备份到: {BACKUP_PATH}")


if __name__ == '__main__':
    migrate()
