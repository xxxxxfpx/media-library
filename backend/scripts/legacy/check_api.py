import requests
import json

response = requests.get("http://localhost:8000/api/media/info?id=3102")
data = response.json()

print(f"Links count: {len(data.get('links', []))}")
print("\nAll links:")
for link in data.get('links', []):
    linked = link.get('linked_item', {})
    print(f"  {link['type']}: id={linked.get('id')}, name={linked.get('name')}")
