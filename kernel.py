import vk_api
from config import ACCESS_TOKEN

def vk_kernel():
    vk_session = vk_api.VkApi(token=ACCESS_TOKEN)

    vk = vk_session.get_api()

    user_info = vk.users.get()

    return user_info