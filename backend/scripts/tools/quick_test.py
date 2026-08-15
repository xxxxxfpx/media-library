import requests

# Login
r = requests.post('http://localhost:8000/api/user/login', json={'username': 'admin', 'password': 'admin123'})
print(f'Login: {r.status_code}')
token = r.json()['access_token']

# Submit rating
r = requests.post('http://localhost:8000/api/user/userdata', headers={'Authorization': f'Bearer {token}'}, json={'item_id': 18587, 'rating': 8.5})
print(f'Submit rating: {r.status_code} {r.json()}')

# Get info
r = requests.get('http://localhost:8000/api/media/info?id=18587', headers={'Authorization': f'Bearer {token}'})
print(f'Get info: {r.status_code}')
if r.status_code == 200:
    data = r.json()
    print(f'Rating: {data.get("userdata", {}).get("rating")}')
else:
    print(f'Error: {r.text[:200]}')
