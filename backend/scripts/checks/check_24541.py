"""检查 ID=24541 的 MediaItem 及其 Season 关联"""
import os
import sqlite3

conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'database', 'media.db'))
cur = conn.cursor()

print("=" * 60)
print("检查 MediaItem ID=24541")
print("=" * 60)

# 1. 查看 MediaItem 24541 的基本信息
print("\n=== MediaItem 24541 信息 ===")
cur.execute('SELECT Id, Type, Name FROM MediaItems WHERE Id = 24541')
row = cur.fetchone()
if row:
    print(f"ID: {row[0]}, Type: {row[1]}, Name: {row[2]}")
else:
    print("❌ MediaItem 24541 不存在")

# 2. 查看 ItemLinks 中与 24541 相关的所有关联
print("\n=== ItemLinks 关联 (ItemId=24541) ===")
cur.execute('''
    SELECT il.LinkedItemId, mi.Name, mi.Type, il.Type
    FROM ItemLinks il
    JOIN MediaItems mi ON il.LinkedItemId = mi.Id
    WHERE il.ItemId = 24541
''')
links_as_item = cur.fetchall()
print(f"作为 ItemId 的关联数量: {len(links_as_item)}")
for link in links_as_item:
    print(f"  LinkedItemId={link[0]}, Type(Link)='{link[3]}', LinkedType='{link[2]}', Name={link[1][:30]}")

# 3. 查看谁关联到了 24541 (作为 LinkedItemId)
print("\n=== ItemLinks 关联 (LinkedItemId=24541) ===")
cur.execute('''
    SELECT il.ItemId, mi.Name, mi.Type, il.Type
    FROM ItemLinks il
    JOIN MediaItems mi ON il.ItemId = mi.Id
    WHERE il.LinkedItemId = 24541
''')
links_as_linked = cur.fetchall()
print(f"作为 LinkedItemId 的关联数量: {len(links_as_linked)}")
for link in links_as_linked:
    print(f"  ItemId={link[0]}, Name={link[1][:30]}, Type='{link[2]}', LinkType='{link[3]}'")

# 4. 检查 24541 是否是 Series
print("\n=== 24541 是否是 Series ===")
cur.execute('SELECT Id, Type, Name FROM MediaItems WHERE Id = 24541 AND Type = "Series"')
if cur.fetchone():
    print("✅ 24541 是 Series 类型")
else:
    print("❌ 24541 不是 Series 类型")

# 5. 检查 24541 是否有 Season 关联 (通过 ItemLinks)
print("\n=== 24541 的 Season 关联 ===")
cur.execute('''
    SELECT il.LinkedItemId, mi.Name, mi.Type
    FROM ItemLinks il
    JOIN MediaItems mi ON il.LinkedItemId = mi.Id
    WHERE il.ItemId = 24541 AND il.Type = 'Season'
''')
season_links = cur.fetchall()
print(f"Season 关联数量: {len(season_links)}")
for s in season_links:
    print(f"  Season ID={s[0]}, Name={s[1]}")

conn.close()
