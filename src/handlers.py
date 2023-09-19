import asyncio
import json
from fastapi import APIRouter

import requests

from src.celery_worker import process_task

@router.post('/') # Тут будет POST метод, потому что будем получать access_token, id или email

async def main_route(info : dict):
    # Отправляем задачу на выполнение в Celery
    result = process_task.delay(info)
    task_result = await get_result(result)
    return {"task_id": result.id, "data": task_result}

async def get_result(result):
    while not result.ready():
        await asyncio.sleep(1)  # Ждем, пока задача не будет завершена
    return result.result
