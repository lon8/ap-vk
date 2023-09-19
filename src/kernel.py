import json
import vk_api
import datetime

from src.config import ACCESS_TOKEN
from src.kernel_functions import get_wall_info, get_posts, get_friends, get_photos

def vk_kernel(search_query):
    vk_session = vk_api.VkApi(token=ACCESS_TOKEN)
    vk = vk_session.get_api()
    user_info = vk.users.get(fields='domain,photo_200_orig,id', user_ids=search_query)[0]

    data = {
        'profile_link': f"https://vk.com/{user_info['domain']}",
        'icon_url': user_info['photo_200_orig'],
        'full_name': f"{user_info['first_name']} {user_info['last_name']}"
    }

    data.update(get_wall_info(vk, user_info['id'], user_info['domain']))

    wall_info = vk.wall.get(count=8, filter='owner', domain=user_info['domain'], extended=True, v=5.131)['items']
    post_id_list = [post['id'] for post in wall_info]
    post_reposts_count = [post['reposts']['count'] for post in wall_info]
    post_date = [post['date'] for post in wall_info]
    post_attachments = [post['attachments'] for post in wall_info]
    post_text = [post['text'] for post in wall_info]

    data['posts'] = get_posts(vk, user_info['id'], post_id_list, post_reposts_count, post_date, post_attachments, post_text)
    data['photos'] = get_photos(vk, user_info['id'])
    data['friends'] = get_friends(vk, user_info['id'])

    final_data = {
        'id': user_info['id'],
        'data': data
    }

    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(final_data, file, indent=4, ensure_ascii=False)

    return final_data
