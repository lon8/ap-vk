from collections import defaultdict
import datetime

# class GetStatistics(APIView):
#     """JSON-ответ с данными статистики по пользователю"""
#     def get(self, request, user_id, format=None):
#         user = request.user
#         # Получение истории поиска по ID
#         search_history = get_object_or_404(AccountSearchHistory, user_id=user_id)
#         total_likes = 0
#         total_comments = 0
#         total_reposts = 0
#         total_views = 0
#         # Проверка прав доступа
#         if not user.is_superuser and not AccountSearchHistory.objects.filter(user_id=user.id).exists():
#             return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

#         start_date_str = request.GET.get('start_date', None)
#         end_date_str = request.GET.get('end_date', None)

#         if start_date_str and end_date_str:
#             histories = AccountSearchHistory.objects.filter(
#                 user_id=user.id,
#                 date__range=(start_date_str, end_date_str)
#             )
#         else:
#             histories = AccountSearchHistory.objects.filter(
#                 user_id=user.id
#             )

#         for search_history in histories:
#             # friends_data = search_history.data.get('data', {}).get('friends', [])
#             # country_stats, city_stats, sex_stats = statistics(friends_data)
#             posts = search_history.data.get('data', {}).get('posts', [])
#             for post in posts:
#                 total_likes += post.get('likes_count', 0)
#                 total_comments += post.get('comments_count', 0)
#                 total_reposts += post.get('reposts_count', 0)
#                 total_views += post.get('view_count', 0)

#         # Выполнение логики статистики
#         friends_data = search_history.data.get('data', {}).get('friends', [])
#         post_data_list = extract_posts_data(post_data)
#         country_stats, city_stats, sex_stats, unique_countries, unique_cities, age_stats = statistics(friends_data)

#         # Извлечение дополнительных данных из поля data
#         additional_data = extract_additional_data(search_history.data)
#         top_likers_list = calculate_likes_views_comments_reposts(post_data)
#         top_commentators_list = calculate_top_commentators(post_data)
#         activity_rating_dict = defaultdict(lambda: {'icon_url': '', 'username': '', 'activity': 0})

#         # Добавляем информацию о лайках
#         for person in top_likers_list:
#             username = person.get('username', None)
#             if username:
#                 activity_rating_dict[username]['icon_url'] = person.get('icon_url', '')
#                 activity_rating_dict[username]['username'] = username
#                 activity_rating_dict[username]['activity'] += person.get('likes_count', 0)

#         # Добавляем информацию о комментариях
#         for person in top_commentators_list:
#             username = person.get('username', None)
#             if username:
#                 activity_rating_dict[username]['icon_url'] = person.get('icon_url', '')
#                 activity_rating_dict[username]['username'] = username
#                 activity_rating_dict[user_id]['activity'] += person.get('comments_count', 0)

#         # Преобразуем словарь обратно в список
#         activity_rating_list = list(activity_rating_dict.values())

#         # Сортируем список по активности
#         activity_rating_list.sort(key=lambda x: x['activity'], reverse=True)

#         # Теперь вы можете добавить этот список в ваш итоговый ответ

#         response_data = {
#             'country_stats': country_stats,
#             'city_stats': city_stats,
#             'sex_stats': sex_stats
#         }
#         response_data.update(additional_data)
        
#         response_data = {
#             'social_network': 1,
#             'posts_count': 0,
#             'followers_count': 0,
#             'follows_count': 0,
#             'likes_count': 0,
#             'comments_count': 0,
#             'views_count': 0,  # Опционально
#             'highlights_count': 0,  # Опционально
#             'mentions_count': 0,  # Опционально
#             'audience': 
#             {
#                 'men_percent': 0,
#                 'women_percent': 0,
#                 'ages': age_stats,
#                 'countries': unique_countries,  # список городов без повторений
#                 'regions': unique_cities, # список стран без повторений
#                 'countries_stats': country_stats,
#                 'regions_stats': city_stats,
#             },
#             'activity_rating':
#             {
#                 'persons': activity_rating_list
#             },
#             'top_likers':
#             {
#                 'persons': top_likers_list
#             },
#             'top_commentators':
#             {
#                 'persons': top_commentators_list
#             },
#             'posts': post_data_list
#         }
        
#         return Response(response_data)
    

from src.statistica import calculate_likes_views_comments_reposts, calculate_top_commentators, extract_additional_data, extract_posts_data, statistics

def calculate_analytics(json_response : dict, uid : int) -> dict:
    total_likes = 0
    total_comments = 0
    total_reposts = 0
    total_views = 0
    
    friends_data = json_response['data']['friends']
    country_stats, city_stats, sex_stats, unique_countries, unique_cities, age_stats = statistics(friends_data)
    
    post_data = json_response['data']['posts']
    post_data_list = extract_posts_data(post_data)
    
    additional_data = extract_additional_data(json_response)
    top_likers_list = calculate_likes_views_comments_reposts(post_data)
    top_commentators_list = calculate_top_commentators(post_data)
    activity_rating_dict = defaultdict(lambda: {'icon_url': '', 'username': '', 'activity': 0})
    
    for person in top_likers_list:
            username = person.get('username', None)
            if username:
                activity_rating_dict[username]['icon_url'] = person.get('icon_url', '')
                activity_rating_dict[username]['username'] = username
                activity_rating_dict[username]['activity'] += person.get('likes_count', 0)
    
    for person in top_commentators_list:
            username = person.get('username', None)
            if username:
                activity_rating_dict[username]['icon_url'] = person.get('icon_url', '')
                activity_rating_dict[username]['username'] = username
                activity_rating_dict[uid]['activity'] += person.get('comments_count', 0)

    activity_rating_list = list(activity_rating_dict.values())
    activity_rating_list.sort(key=lambda x: x['activity'], reverse=True)
    
    response_data = {
        'country_stats': country_stats,
        'city_stats': city_stats,
        'sex_stats': sex_stats,
        'date': str(datetime.datetime.now()),
        'social_network': 1,
        'posts_count': 0,
        'followers_count': 0,
        'follows_count': 0,
        'likes_count': 0,
        'comments_count': 0,
        'views_count': 0,  # Опционально
        'highlights_count': 0,  # Опционально
        'mentions_count': 0,  # Опционально
        'audience': 
        {
            'men_percent': 0,
            'women_percent': 0,
            'ages': age_stats,
            'countries': unique_countries,  # список городов без повторений
            'regions': unique_cities, # список стран без повторений
            'countries_stats': country_stats,
            'regions_stats': city_stats,
        },
        'activity_rating':
        {
            'persons': activity_rating_list
        },
        'top_likers':
        {
            'persons': top_likers_list
        },
        'top_commentators':
        {
            'persons': top_commentators_list
        },
        'posts': post_data_list
    }
    
    response_data.update(additional_data)
    
    return response_data