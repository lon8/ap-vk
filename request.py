import requests

json = {
    'uid': '515518132'
}

req = requests.post('http://127.0.0.1:8000/', json=json, verify=False)