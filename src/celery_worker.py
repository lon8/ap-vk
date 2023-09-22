import json
from celery import Celery
from src.kernel import vk_kernel
from src.views import calculate_analytics

celery = Celery(
    'myapp',
    broker='redis://localhost:6379/0',  # URL Redis сервера для Celery
    backend='redis://localhost:6379/0'  # URL Redis сервера для результатов выполнения задач
    )

json_data = {}


@celery.task()
def process_task(info : dict):
    result = vk_kernel(info['search_query'])
    
    result_stats = calculate_analytics(result, info['user_id'])
    json_data['search_query'] = info['search_query']
    json_data['data'] = result_stats
    
    return json_data

if __name__ == '__main__':
    celery.start()
