from fastapi import APIRouter
from kernel import vk_kernel


router = APIRouter()

# Пример 

# data = {
#   access_token: # Тут по-хорошему надо шифроваться
#   vkuserId: # или ID пользователя, или Email
#   userId: # ID пользователя из нашего сервиса
# }

@router.get('/get_data') # Тут будет POST метод, потому что будем получать access_token,
                         #id или email пользователя
def main_route():
    result = vk_kernel()
    return result
