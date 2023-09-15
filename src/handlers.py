from fastapi import APIRouter
from src.kernel import vk_kernel
import requests

headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk0ODMwMTg5LCJpYXQiOjE2OTQ3NDM3ODksImp0aSI6ImFhYjBhZWIxNmQ2MzQ3OGViMjA4MDI3MmI5Y2JhNTRkIiwidXNlcl9pZCI6NTh9.4KBSbdjmterjxCAXRspSdAbh-b-MthS7-aBFyT9Hx7M',
}

json_data = {
    'search_query': 'some_search_query',
}

router = APIRouter()

# Пример 

# data = {
#   uid: our id
# }

@router.post('/') # Тут будет POST метод, потому что будем получать access_token,
                         #id или email пользователя
def main_route(info : dict):
    result = vk_kernel(info['search_query'])
    json_data['data'] = result
    response = requests.post(f'http://88.218.60.146/api/add_history/{info["social"]}/{info["user_id"]}/', headers=headers, json=json_data)
    return result