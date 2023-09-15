import json
import vk_api
from src.config import ACCESS_TOKEN
import datetime



def get_user_info(vk : vk_api.vk_api, uid_list : list[str]):
    users = vk.users.get(fields='photo_200_orig,domain', user_ids=uid_list)
    for user in users:
        user['profile_link'] = f"https://vk.com/{user['domain']}"
        user['icon_url'] = user['photo_200_orig']
        del user['photo_200_orig']
    return users

def vk_kernel(user_id : str):
    vk_session = vk_api.VkApi(token=ACCESS_TOKEN)

    final_data = {}

    vk = vk_session.get_api()

    data = {}
    
    user_info = vk.users.get(fields='domain,photo_200_orig', user_ids=f'{user_id}')[0]
    profile_link = f"https://vk.com/{user_info['domain']}"
    avatar_link = user_info['photo_200_orig']
    full_name = f"{user_info['first_name']} {user_info['last_name']}"

    data['profile_link'] = profile_link
    data['icon_url'] = avatar_link
    data['full_name'] = full_name

    # # Получение количества друзей и подписчиков
    friends_count = vk.friends.get()['count']
    followers_count = vk.users.getFollowers()['count']
    data['friends_count'] = friends_count
    data['followers_count'] = followers_count

    total_posts : int = 0
    total_views : int = 0
    total_likes : int = 0
    total_comments : int = 0
    total_reposts : int = 0
    
    # Получение информации о стенах пользователя
    for i in range(0, 1000000, 100):
        wall_info : dict = vk.wall.get(count=100, filter='owner', offset=i)['items']
        total_posts += len(wall_info)
        
        data['total_posts'] = total_posts
        
        total_views += sum(post['views']['count'] for post in wall_info)
        total_likes += sum(post['likes']['count'] for post in wall_info)
        total_reposts += sum(post['reposts']['count'] for post in wall_info)
        total_comments += sum(post['comments']['count'] for post in wall_info)
        
        if i == 0:
            data['total_views'] = total_views
            data['total_likes'] = total_likes
            data['total_reposts'] = total_reposts
            data['total_comments'] = total_comments
        else:
            data['total_views'] += total_views
            data['total_likes'] += total_likes
            data['total_reposts'] += total_reposts
            data['total_comments'] += total_comments
        if len(wall_info) == 0 or len(wall_info) < 100:
            break
        
    wall_info : dict = vk.wall.get(count=8, filter='owner', offset=i)['items']
    # Списки
    post_id_list : list = [post['id'] for post in wall_info]
    post_views_count : list = [post['views']['count'] for post in wall_info]
    post_reposts_count : list = [post['reposts']['count'] for post in wall_info]
    post_date : list = [post['date'] for post in wall_info]
    post_attachments : list = [post['attachments'] for post in wall_info]

    
    posts = []
    for postnum, post_id in enumerate(post_id_list, start=0):
        post = {}
        
        normal_date = datetime.datetime.fromtimestamp(post_date[postnum])

        post['date'] = str(normal_date)
        post['view_count'] = post_views_count[postnum]
        post['reposts_count'] = post_reposts_count[postnum]
        
        # Собираем комментарии
        comments = vk.wall.getComments(post_id=post_id, count=100, fields='id,domain,first_name,last_name,photo_200_orig',extended=1)
        post['comments_count'] = comments['count']
        if comments['count'] == 0:
            profiles_comments = comments['profiles']
        else:
            profiles_comments = [profile for profile in comments['profiles']]
        
        post['commentators'] = profiles_comments
        
        # Собираем лайки
        likes = vk.wall.getLikes(count=1000, post_id=post_id)
        post['likers'] = likes

        likers_str = ','.join([str(user['uid']) for user in post['likers']['users']])

        post['likers'] = get_user_info(vk, likers_str)

        post['likes_count'] = len(post['likers'])

        attachments = []

        for attachment in post_attachments[postnum]:
            if attachment['type'] == 'photo':
                post_photo = attachment['photo']['sizes'][-1]
                attachments.append(post_photo)

        post['photos'] = attachments

        posts.append(post)
    
    data['posts'] = posts


    # Получение данных о фотографиях пользователя
    photos_info = vk.photos.getAll(count=100, album_id='profile', extended=1)['items']
    photos = []

    for ph in photos_info:
        photo = {}

        photo['date'] = str(datetime.datetime.fromtimestamp(ph['date']))
        photo['likes'] = ph['likes']['count']
        try:
            photo['comments'] = ph['comments']['count']
        except:
            photo['comments'] = 0
        photo['reposts'] = ph['likes']['count']
        photo['url'] = ph['sizes'][-1]['url'] # Здесь используем -1 для взятия максимального размера фотографии

        photos.append(photo)

    data['photos'] = photos

    # Получение данных о друзьях пользователя
    friends_info_list = vk.friends.get(fields='domain,photo_200_orig,country,city,bdate,sex', count=10000)['items']
    
    friends = []

    for friend_info in friends_info_list:
        friend = {}
        friend['profile_link'] = f"https://vk.com/{friend_info['domain']}"
        try:
            friend['bdate'] = friend_info['bdate']
        except:
            friend['bdate'] = ''
        try:
            friend['city'] = friend_info['city']['title']
        except:
            friend['city'] = ''
        try:
            friend['country'] = friend_info['country']['title']
        except:
            friend['country'] = ''
        friend['icon_url'] = friend_info['photo_200_orig']
        del friend_info['photo_200_orig']
        try:
            if friend_info['sex'] == 1:
                friend['sex'] = 'Female'
            else: friend['sex'] = 'Male'
        except:
            friend['sex'] = ''

        friends.append(friend)

    data['friends'] = friends
    
    final_data['id'] = user_info['id']
    final_data['data'] = data

    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(final_data, file, indent=4, ensure_ascii=False)

    return final_data

    # Statistics