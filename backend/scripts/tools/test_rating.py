# coding: utf-8
"""
测试用户评分功能
"""

import requests
import json

BASE_URL = 'http://localhost:8000'

print("=" * 60)
print("测试用户评分功能")
print("=" * 60)

# 1. 登录获取 token
print("\n1. 登录获取 token")
r = requests.post(f'{BASE_URL}/api/user/login', json={'username': 'admin', 'password': 'admin123'})
if r.status_code != 200:
    print(f"   ❌ 登录失败：{r.status_code}")
    print(f"   响应：{r.text[:200]}")
    exit(1)
    
print(f"   ✓ 状态码：{r.status_code}")
token = r.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}

# 2. 获取第一个收藏的媒体
print("\n2. 获取收藏列表")
r = requests.get(f'{BASE_URL}/api/media/list?favorite=true&limit=1', headers=headers)
print(f"   状态码：{r.status_code}")

if r.status_code != 200:
    print(f"   ❌ 请求失败：{r.text[:200]}")
    exit(1)

data = r.json()
print(f"   总数：{data['total']}")

if not data['items']:
    print("   ❌ 没有收藏记录，测试终止")
    exit(1)

item = data['items'][0]
item_id = item['id']
item_name = item['name']
print(f"   ✓ 测试媒体：{item_name} (ID: {item_id})")

# 获取当前评分
current_rating = item.get('userdata', {}).get('rating')
print(f"   当前评分：{current_rating}")

# 3. 提交评分
print("\n3. 提交评分 (rating=8.5)")
r = requests.post(
    f'{BASE_URL}/api/user/userdata',
    headers=headers,
    json={
        'item_id': item_id,
        'rating': 8.5
    }
)
print(f"   状态码：{r.status_code}")
print(f"   响应：{r.json()}")

if r.status_code != 200:
    print(f"   ❌ 提交评分失败")
    exit(1)

# 4. 验证评分已保存
print("\n4. 验证评分已保存")
r = requests.get(f'{BASE_URL}/api/media/info?id={item_id}', headers=headers)
print(f"   状态码：{r.status_code}")

if r.status_code == 200:
    new_item = r.json()
    new_rating = new_item.get('userdata', {}).get('rating')
    print(f"   新评分：{new_rating}")
    
    if new_rating == 8.5:
        print("   ✓ 评分保存成功！")
    else:
        print(f"   ❌ 评分保存失败！期望 8.5，实际 {new_rating}")
else:
    print(f"   ❌ 请求失败：{r.text[:200]}")

# 5. 修改评分
print("\n5. 修改评分 (rating=9.0)")
r = requests.post(
    f'{BASE_URL}/api/user/userdata',
    headers=headers,
    json={
        'item_id': item_id,
        'rating': 9.0
    }
)
print(f"   状态码：{r.status_code}")
print(f"   响应：{r.json()}")

# 6. 验证评分已更新
print("\n6. 验证评分已更新")
r = requests.get(f'{BASE_URL}/api/media/info?id={item_id}', headers=headers)
print(f"   状态码：{r.status_code}")

if r.status_code == 200:
    updated_item = r.json()
    updated_rating = updated_item.get('userdata', {}).get('rating')
    print(f"   更新后评分：{updated_rating}")
    
    if updated_rating == 9.0:
        print("   ✓ 评分更新成功！")
    else:
        print(f"   ❌ 评分更新失败！期望 9.0，实际 {updated_rating}")
else:
    print(f"   ❌ 请求失败：{r.text[:200]}")

# 7. 验证收藏列表返回评分
print("\n7. 验证收藏列表返回评分")
r = requests.get(f'{BASE_URL}/api/media/list?favorite=true&limit=5', headers=headers)
if r.status_code == 200:
    data = r.json()
    print(f"   状态码：{r.status_code}")
    for item in data['items'][:3]:
        rating = item.get('userdata', {}).get('rating')
        print(f"   - {item['name']}: rating={rating}")
else:
    print(f"   ❌ 请求失败：{r.status_code}")

print("\n" + "=" * 60)
print("测试完成！")
print("=" * 60)
