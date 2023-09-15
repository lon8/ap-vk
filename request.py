import json
import requests

json_data = {
    'search_query': '515518132',
    'user_id': 52,
}


req = requests.post('http://127.0.0.1:8000/', json=json_data, verify=False)
# req = requests.post('http://88.210.14.5:8000/', json=json_data, verify=False)

with open('YES.json', 'w', encoding='utf-8') as file:
    json.dump(req.json(), file, indent=4, ensure_ascii=False)