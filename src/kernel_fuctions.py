def get_posts(vk, user_id, post_id_list, post_reposts_count, post_date, post_attachments, post_text):
    posts = []
    for postnum, post_id in enumerate(post_id_list, start=0):
        post = {}

        normal_date = datetime.datetime.fromtimestamp(post_date[postnum])

        post['date'] = str(normal_date)
        post['reposts_count'] = post_reposts_count[postnum]

        # Собираем комментарии
        comments = vk.wall.getComments(owner_id=user_id, post_id=post_id, count=100,
                                       fields='id,domain,first_name,last_name,photo_200_orig', extended=1)
        post['comments_count'] = comments['count']
        if comments['count'] == 0:
            profiles_comments = comments['profiles']
        else:
            profiles_comments = [profile for profile in comments['profiles']]

        post['commentators'] = profiles_comments

        # Собираем лайки
        likes = vk.wall.getLikes(owner_id=user_id, count=1000, post_id=post_id)
        post['likers'] = likes

        likers_str = ','.join([str(user['uid']) for user in post['likers']['users']])

        post['likers'] = get_user_info(vk, likers_str)

        post['likes_count'] = len(post['likers'])

        post['text'] = post_text[postnum]

        attachments = []

        for attachment in post_attachments[postnum]:
            if attachment['type'] == 'photo':
                post_photo = attachment['photo']['sizes'][-1]
                attachments.append(post_photo)

        post['media'] = attachments

        posts.append(post)

    return posts

def get_photos(vk, user_id):
    photos_info = vk.photos.getAll(owner_id=user_id, count=100, album_id='profile', extended=1)['items']
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
        photo['url'] = ph['sizes'][-1]['url']

        photos.append(photo)

    return photos

def get_friends(vk, user_id):
    friends_info_list = vk.friends.get(user_id=user_id,
                                       fields='domain,photo_200_orig,country,city,bdate,sex', count=10000)['items']

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
            else:
                friend['sex'] = 'Male'
        except:
            friend['sex'] = ''

        friends.append(friend)

    return friends
