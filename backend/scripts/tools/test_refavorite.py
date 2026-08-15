# coding: utf-8
"""
测试重新收藏时更新 FavoritedAt
"""

import requests
import time
import json

BASE_URL = 'http://localhost:8000'

# 登录获取 token
r = requests.post(f'{BASE_URL}/api/user/login', json={'username': 'admin', 'password': 'admin123'})
token = r.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}

print("=" * 60)
print("测试重新收藏时更新 FavoritedAt")
print("=" * 60)

# 获取第一个收藏的媒体
r = requests.get(f'{BASE_URL}/api/media/list?favorite=true&sort_by=favorited_at', headers=headers)
data = r.json()

if not data['items']:
    print("❌ 没有收藏记录，请先收藏一个媒体")
    exit(1)

item = data['items'][0]
item_id = item['id']
item_name = item['name']
old_favorited_at = item['userdata']['favorited_at'] if item.get('userdata') else None

print(f"\n测试媒体：{item_name} (ID: {item_id})")
print(f"收藏前：{old_favorited_at}")

# 取消收藏
print("\n1. 取消收藏...")
r = requests.post(
    f'{BASE_URL}/api/user/userdata',
    headers=headers,
    json={
        'item_id': item_id,
        'is_favorite': False
    }
)
print(f"   状态：{r.json().get('message', '成功')}")

# 等待 2 秒
print("\n   等待 2 秒...")
time.sleep(2)

# 重新收藏
print("\n2. 重新收藏...")
r = requests.post(
    f'{BASE_URL}/api/user/userdata',
    headers=headers,
    json={
        'item_id': item_id,
        'is_favorite': True
    }
)
print(f"   状态：{r.json().get('message', '成功')}")

# 获取最新收藏时间
print("\n3. 获取最新收藏时间...")
r = requests.get(f'{BASE_URL}/api/media/info?id={item_id}', headers=headers)
new_item = r.json()
new_favorited_at = new_item['userdata']['favorited_at'] if new_item.get('userdata') else None
print(f"   收藏后：{new_favorited_at}")

# 验证
print("\n" + "=" * 60)
print("验证结果")
print("=" * 60)
if old_favorited_at and new_favorited_at:
    if new_favorited_at > old_favorited_at:
        print(f"✓ 成功！收藏时间已更新")
        print(f"  旧时间：{old_favorited_at}")
        print(f"  新时间：{new_favorited_at}")
    elif new_favorited_at == old_favorited_at:
        print(f"❌ 失败！收藏时间未更新")
        print(f"  时间：{new_favorited_at}")
    else:
        print(f"❌ 异常！新时间比旧时间还早")
        print(f"  旧时间：{old_favorited_at}")
        print(f"  新时间：{new_favorited_at}")
else:
    print(f"❌ 无法获取收藏时间")
    print(f"  旧：{old_favorited_at}, 新：{new_favorited_at}")

print("=" * 60)
