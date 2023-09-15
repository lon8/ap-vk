import asyncio
import json
from fastapi import APIRouter

import requests

from src.celery_worker import process_task

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
async def main_route(info : dict):
    # Отправляем задачу на выполнение в Celery
    result = process_task.delay(info)
    task_result = await get_result(result)
    return {"task_id": result.id, "data": task_result}

async def get_result(result):
    while not result.ready():
        await asyncio.sleep(1)  # Ждем, пока задача не будет завершена
    return result.result