# coding: utf-8
"""
测试 FavoritedAt 功能
"""

import requests
import json

BASE_URL = 'http://localhost:8000'

# 1. 登录获取 token
print("=" * 60)
print("1. 登录获取 token")
print("=" * 60)
r = requests.post(f'{BASE_URL}/api/user/login', json={'username': 'admin', 'password': 'admin123'})
print(f"状态码：{r.status_code}")
print(f"响应：{r.json()}")
token = r.json()['access_token']
print(f"Token: {token[:50]}...\n")

# 2. 获取收藏列表（按 favorited_at 排序）
print("=" * 60)
print("2. 获取收藏列表（按 favorited_at 排序）")
print("=" * 60)
r = requests.get(
    f'{BASE_URL}/api/media/list?favorite=true&sort_by=favorited_at',
    headers={'Authorization': f'Bearer {token}'}
)
print(f"状态码：{r.status_code}")
data = r.json()
print(f"总数：{data['total']}")
print(f"返回 {len(data['items'])} 条记录\n")

# 3. 检查是否返回 favorited_at 字段
print("=" * 60)
print("3. 检查 favorited_at 字段")
print("=" * 60)
if data['items']:
    item = data['items'][0]
    print(f"第一个媒体：{item['name']}")
    if item.get('userdata'):
        ud = item['userdata']
        print(f"  is_favorite: {ud.get('is_favorite')}")
        print(f"  favorited_at: {ud.get('favorited_at')}")
        print(f"  last_played_date: {ud.get('last_played_date')}")
        
        # 验证字段存在
        assert 'favorited_at' in ud, "❌ favorited_at 字段缺失！"
        print("\n✓ favorited_at 字段存在！")
    else:
        print("  无 userdata")
else:
    print("没有收藏记录")

# 4. 验证排序（按 favorited_at 倒序）
print("\n" + "=" * 60)
print("4. 验证排序（应该按 favorited_at 倒序）")
print("=" * 60)
if len(data['items']) > 1:
    dates = []
    for item in data['items']:
        if item.get('userdata') and item['userdata'].get('favorited_at'):
            dates.append(item['userdata']['favorited_at'])
    
    if dates:
        print(f"收藏时间列表（应该从新到旧）:")
        for i, d in enumerate(dates[:5], 1):
            print(f"  {i}. {d}")
        
        # 验证是否降序
        is_desc = all(dates[i] >= dates[i+1] for i in range(len(dates)-1))
        if is_desc:
            print("\n✓ 排序正确（降序）！")
        else:
            print("\n❌ 排序错误（不是降序）！")
    else:
        print("没有足够的 favorited_at 数据进行排序验证")
else:
    print("收藏记录不足 2 条，无法验证排序")

print("\n" + "=" * 60)
print("测试完成！")
print("=" * 60)
