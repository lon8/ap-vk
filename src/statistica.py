from collections import Counter
from datetime import datetime


def calculate_age(bdate: str, current_year: int) -> int:
    day, month, year = map(int, bdate.split('.'))
    return current_year - year


def statistics(friends_data) -> tuple:
    current_year = datetime.now().year
    country_counter = Counter()
    city_counter = Counter()
    sex_counter = Counter()
    age_counter = Counter()
    unique_countries = set()
    unique_cities = set()

    for friend in friends_data:
        country = friend.get('country', None)
        city = friend.get('city', None)
        sex = friend.get('sex', None)

        if country:
            country_counter[country] += 1
            unique_countries.add(country)

        if city:
            city_counter[city] += 1
            unique_cities.add(city)

        if sex:
            sex_counter[sex] += 1

        bdate = friend.get('bdate', None)
        if bdate:
            try:
                age = calculate_age(bdate, current_year)
                if age < 14:
                    age_counter['less_14'] += 1
                elif age < 19:
                    age_counter['14_18'] += 1
                elif age < 25:
                    age_counter['18_24'] += 1
                elif age < 35:
                    age_counter['25_34'] += 1
                elif age < 45:
                    age_counter['35_44'] += 1
                else:
                    age_counter['45_54'] += 1
            except ValueError:
                pass  # Invalid date format

    def total_count(counter):
        return sum(counter.values())

    def rounded_stats(counter):
        return {key: round((value / total_count(counter)) * 100) for key, value in counter.items()}

    return (
        rounded_stats(country_counter),
        rounded_stats(city_counter),
        rounded_stats(sex_counter),
        list(unique_countries),
        list(unique_cities),
        rounded_stats(age_counter)
    )

def find_index_by_value(array_of_dicts, target_value):
    for index, dictionary in enumerate(array_of_dicts):
        for key, value in dictionary.items():
            if value == target_value:
                return index
    return -1  # Вернуть -1, если значение не найдено в массиве

def extract_additional_data(data_json) -> dict:
    additional_data = data_json
    result = {
        'profile_link': additional_data.get('profile_link', ''),
        'avatar_link': additional_data.get('icon_url', ''),
        'full_name': additional_data.get('full_name', ''),
        'follows_count': additional_data.get('friends_count', 0),
        'followers_count': additional_data.get('followers_count', 0),
        'posts_count': additional_data.get('total_posts', 0),
        'likes_count': additional_data.get('total_likes', 0),
        'reposts_count': additional_data.get('total_reposts', 0),
        'comments_count': additional_data.get('total_comments', 0),
    }
    
    return result

def extract_posts_data(raw_posts) -> list:
    processed_posts = []

    for post in raw_posts:
        post_data = {}
        post_data['photos'] = post['media']
        post_data['text'] = ''  # Текст поста (если есть)
        # post_data['views_count'] = post.get('view_count', 0)
        post_data['likes_count'] = post.get('likes_count', 0)
        post_data['comments_count'] = post.get('comments_count', 0)
        post_data['reposts_count'] = post.get('reposts_count', 0)  # Опционально
        post_data['date'] = post.get('date', '')

        processed_posts.append({'data': post_data})

    return processed_posts


# функция подсчета лайков, просмотров, комментариев и репостов
def calculate_likes_views_comments_reposts(posts_data):
    likers_counter = Counter()

    if isinstance(posts_data, list):
        posts = posts_data
    elif isinstance(posts_data, dict) and 'posts' in posts_data:
        posts = posts_data['posts']
    else:
        print("Неподдерживаемый формат данных")
        return []
    
    all_likers = []
    for post in posts:
        likers = post.get("likers", [])
        all_likers = all_likers + likers
        for liker in likers:
            likers_counter[liker["domain"]] += 1

    top_10_likers = likers_counter.most_common(10)

    top_likers_list = []
    for domain, count in top_10_likers:
        value = find_index_by_value(all_likers, domain)
        
        top_likers_list.append({
            'icon_url': all_likers[value]['icon_url'],  # Здесь должна быть ссылка на аватар пользователя, если есть
            'username': f"{all_likers[value]['first_name']} {all_likers[value]['last_name']}",
            'likes_count': count
        })

    return top_likers_list


def calculate_top_commentators(posts_data) -> list:
    """Функция подсчета топ-10 комментаторов"""
    commentators_counter = Counter()

    # Словарь для хранения информации о комментаторах по их ID
    all_commentators = []
    for post in posts_data:
        for commentator in post.get('commentators', []):
            commentators = post.get("commentators", [])
            all_commentators = all_commentators + commentators
            for commentator in commentators:
                commentators_counter[commentator["domain"]] += 1
            
    top_10_commentators = commentators_counter.most_common(10)
    
    top_commentators_list = []
    for domain, count in top_10_commentators:
        value = find_index_by_value(all_commentators, domain)
        
        top_commentators_list.append({
            'icon_url': all_commentators[value]['photo_200_orig'],
            'username': f"{all_commentators[value]['first_name']} {all_commentators[value]['last_name']}",
            'comments_count': count
        })

    return top_commentators_list
#