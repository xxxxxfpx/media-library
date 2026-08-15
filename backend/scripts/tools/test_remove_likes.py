# coding: utf-8
"""
测试移除 Likes 字段后的功能
"""

import requests
import json

BASE_URL = 'http://localhost:8000'

print("=" * 60)
print("测试移除 Likes 字段后的功能")
print("=" * 60)

# 1. 登录获取 token
print("\n1. 登录获取 token")
r = requests.post(f'{BASE_URL}/api/user/login', json={'username': 'admin', 'password': 'admin123'})
print(f"   状态码：{r.status_code}")
token = r.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}

# 2. 获取收藏列表
print("\n2. 获取收藏列表（按 favorited_at 排序）")
r = requests.get(f'{BASE_URL}/api/media/list?favorite=true&sort_by=favorited_at', headers=headers)
print(f"   状态码：{r.status_code}")
data = r.json()
print(f"   总数：{data['total']}")
print(f"   返回 {len(data['items'])} 条记录")

# 3. 检查 userdata 中是否不包含 likes 字段
print("\n3. 检查 userdata 字段")
if data['items']:
    item = data['items'][0]
    if item.get('userdata'):
        ud = item['userdata']
        print(f"   userdata 键：{list(ud.keys())}")
        
        # 验证不包含 likes
        if 'likes' in ud:
            print(f"   ❌ 错误：userdata 仍然包含 likes 字段")
        else:
            print(f"   ✓ 正确：userdata 不包含 likes 字段")
        
        # 验证包含必要字段
        required_fields = ['is_favorite', 'playback_position_ticks', 'favorited_at']
        for field in required_fields:
            if field in ud:
                print(f"   ✓ 包含 {field}")
            else:
                print(f"   ❌ 缺少 {field}")
    else:
        print("   无 userdata")

# 4. 测试更新用户数据
print("\n4. 测试更新用户数据（取消收藏再收藏）")
if data['items']:
    item_id = data['items'][0]['id']
    
    # 取消收藏
    r = requests.post(
        f'{BASE_URL}/api/user/userdata',
        headers=headers,
        json={'item_id': item_id, 'is_favorite': False}
    )
    print(f"   取消收藏：{r.status_code}")
    
    # 重新收藏
    r = requests.post(
        f'{BASE_URL}/api/user/userdata',
        headers=headers,
        json={'item_id': item_id, 'is_favorite': True}
    )
    print(f"   重新收藏：{r.status_code}")
    print(f"   响应：{r.json()}")

print("\n" + "=" * 60)
print("测试完成！")
print("=" * 60)
