"""检查 ID=24541 的详细信息和关联"""
import os
import sqlite3

conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'database', 'media.db'))
cur = conn.cursor()

print("=" * 60)
print("检查 ID=24541 的详细信息和关联")
print("=" * 60)

# 1. 查看 MediaItem 24541 的信息
print("\n=== MediaItem 24541 ===")
cur.execute('SELECT Id, Type, Name FROM MediaItems WHERE Id = 24541')
row = cur.fetchone()
if row:
    print(f"ID: {row[0]}, Type: {row[1]}, Name: {row[2]}")
else:
    print("❌ 不存在")
    conn.close()
    exit()

# 2. 查看 24541 的所有 ItemLinks
print("\n=== ItemLinks (ItemId=24541) ===")
cur.execute('''
    SELECT il.LinkedItemId, mi.Type, mi.Name, il.Type
    FROM ItemLinks il
    JOIN MediaItems mi ON il.LinkedItemId = mi.Id
    WHERE il.ItemId = 24541
''')
links = cur.fetchall()
print(f"作为 ItemId 的关联数量: {len(links)}")
for link in links:
    print(f"  LinkedItemId={link[0]}, LinkedType={link[1]}, Name={link[2][:30]}, LinkType={link[3]}")

# 3. 查看谁关联到了 24541 (作为 LinkedItemId)
print("\n=== ItemLinks (LinkedItemId=24541) ===")
cur.execute('''
    SELECT il.ItemId, mi.Type, mi.Name, il.Type
    FROM ItemLinks il
    JOIN MediaItems mi ON il.ItemId = mi.Id
    WHERE il.LinkedItemId = 24541
''')
reverse_links = cur.fetchall()
print(f"作为 LinkedItemId 的关联数量: {len(reverse_links)}")
for link in reverse_links:
    print(f"  ItemId={link[0]}, Type={link[1]}, Name={link[2][:30]}, LinkType={link[3]}")

# 4. 检查这个 Season 24748 是什么
print("\n=== 检查 Season 24748 ===")
cur.execute('SELECT Id, Type, Name FROM MediaItems WHERE Id = 24748')
season = cur.fetchone()
if season:
    print(f"ID: {season[0]}, Type: {season[1]}, Name: {season[2]}")

conn.close()
