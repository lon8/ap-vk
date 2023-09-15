import requests

json_data = {
    'search_query': '515518132',
    'user_id': 52,
}

req = requests.post('http://127.0.0.1:8000/', json=json_data, verify=False)
