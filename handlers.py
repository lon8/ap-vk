from fastapi import APIRouter
from kernel import vk_kernel


router = APIRouter()

# Пример 

# data = {
#   uid: our id
# }

@router.post('/') # Тут будет POST метод, потому что будем получать access_token,
                         #id или email пользователя
def main_route(info : dict):
    result = vk_kernel(info['uid'])
    return result
