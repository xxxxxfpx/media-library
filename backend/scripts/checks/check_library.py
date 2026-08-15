"""检查图书馆数据"""
import requests
import json

# 检查后端 API
print("检查后端 API...")
try:
    response = requests.get("http://localhost:8000/api/media/list?limit=10")
    data = response.json()
    print(f"状态码: {response.status_code}")
    print(f"总数: {data.get('total', 0)}")
    print(f"返回条数: {len(data.get('items', []))}")
    for item in data.get('items', [])[:5]:
        print(f"  {item['id']}: {item['name']} ({item.get('type', 'unknown')})")
except Exception as e:
    print(f"错误: {e}")
