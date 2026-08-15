"""检查 Source 类型数据"""
import requests

print("检查 Source 类型数据...")
try:
    response = requests.get("http://localhost:8000/api/media/list?types=Source&limit=50")
    data = response.json()
    print(f"状态码: {response.status_code}")
    print(f"总数: {data.get('total', 0)}")
    print(f"返回条数: {len(data.get('items', []))}")
    for item in data.get('items', []):
        print(f"  {item['id']}: {item['name']} ({item.get('type', 'unknown')})")
except Exception as e:
    print(f"错误: {e}")
