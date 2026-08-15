import json
import sys

d = json.load(sys.stdin)
print('files count:', len(d.get('files', [])))
for f in d.get('files', []):
    print(f"  {f['id']}: {f['path']} ({f.get('image_type', 'none')})")
