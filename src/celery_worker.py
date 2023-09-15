import json
from celery import Celery
from src.kernel import vk_kernel
from src.views import calculate_analytics

celery = Celery(
    'myapp',
    broker='redis://localhost:6379/0',  # URL Redis сервера для Celery
    backend='redis://localhost:6379/0'  # URL Redis сервера для результатов выполнения задач
)

json_data = {
    'search_query': 'some_search_query',
}


@celery.task()
def process_task(info : dict):
    result = vk_kernel(info['search_query'])
    
    result_stats = calculate_analytics(result, info['user_id'])
    
    json_data['data'] = result_stats
    # response = requests.post(f'http://88.218.60.146/api/add_history/{info["social"]}/{info["user_id"]}/', headers=headers, json=json_data)
    
    with open('stats_result.json', 'w', encoding='utf-8') as file:
        json.dump(json_data, file, indent=4, ensure_ascii=False)
        
    return json_data

if __name__ == '__main__':
    celery.start()