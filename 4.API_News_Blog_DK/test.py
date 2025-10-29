# #СОЗДАНИЕ СТАТЬИ

# import requests
# session = requests.Session()
# login_data = {
#     'email': 'mrdmitry2006@mail.ru',
#     'password': '123456'
# }
# login_response = session.post('http://127.0.0.1:5000/login', data=login_data)
# print(f"Авторизация: {login_response.status_code}")

# create_data = {
#     "title": "Статья через API",
#     "text": "Тестовая статья через API",
#     "category": "Технологии"
# }

# response = session.post(
#     "http://127.0.0.1:5000/api/articles",
#     json=create_data
# )

# print("Результат создания статьи:")
# print(f"Статус: {response.status_code}")
# print(f"Ответ: {response.json()}")


# # РЕДАКТИРОВАНИЕ СТАТЬИ

# import requests

# session = requests.Session()

# login_data = {
#     'email': 'mrdmitry2006@mail.ru',
#     'password': '123456'
# }
# login_response = session.post('http://127.0.0.1:5000/login', data=login_data)
# print(f"Авторизация: {login_response.status_code}")

# articles_response = session.get("http://127.0.0.1:5000/api/articles")
# if articles_response.status_code == 200:
#     articles = articles_response.json()
    

# update_data = {
#     "title": "ОТРЕДАКТИРОВАННАЯ статья через API c 4 id",
#     "text": "Этот текст был полностью изменен через API запрос",
#     "category": "Обновленная категория"
# }

# article_id = 4
# response = session.put(
#     f"http://127.0.0.1:5000/api/articles/{article_id}",
#     json=update_data
# )

# print(f"\nРезультат редактирования статьи ID {article_id}:")
# print(f"Статус: {response.status_code}")
# result = response.json()
# print(f"Ответ: {result}")

# #УДАЛЕНИЕ СТАТЬИ

# import requests

# session = requests.Session()

# login_data = {
#     'email': 'mrdmitry2006@mail.ru',
#     'password': '123456'
# }
# login_response = session.post('http://127.0.0.1:5000/login', data=login_data)
# print(f"Авторизация: {login_response.status_code}")

# articles_response = session.get("http://127.0.0.1:5000/api/articles")
# if articles_response.status_code == 200:
#     articles = articles_response.json()

# article_id = 4
# response = session.delete(
#     f"http://127.0.0.1:5000/api/articles/{article_id}"
# )

# print(f"\nРезультат удаления статьи ID {article_id}:")
# print(f"Статус: {response.status_code}")
# result = response.json()
# print(f"Ответ: {result}")

# #СОЗДАНИЕ КОММЕНТАРИЯ

# import requests

# session = requests.Session()

# login_data = {
#     'email': 'mrdmitry2006@mail.ru',
#     'password': '123456'
# }
# login_response = session.post('http://127.0.0.1:5000/login', data=login_data)
# print(f"Авторизация: {login_response.status_code}")

# articles_response = session.get("http://127.0.0.1:5000/api/articles")
# if articles_response.status_code == 200:
#     articles = articles_response.json()
#     print("Доступные статьи:")
#     for article in articles['articles']:
#         print(f"  ID: {article['id']} - '{article['title']}'")

# comment_data = {
#     "text": "Этот комментарий был создан с API",
#     "article_id": 1
# }

# response = session.post(
#     "http://127.0.0.1:5000/api/comment",
#     json=comment_data
# )

# print("\nРезультат создания комментария:")
# print(f"Статус: {response.status_code}")
# print(f"Ответ: {response.json()}")

# #РЕДАКТИРОВАНИЕ КОММЕНТА

# import requests

# session = requests.Session()

# login_data = {
#     'email': 'mrdmitry2006@mail.ru',
#     'password': '123456'
# }
# login_response = session.post('http://127.0.0.1:5000/login', data=login_data)
# print(f"Авторизация: {login_response.status_code}")

# comments_response = session.get("http://127.0.0.1:5000/api/comment")
# if comments_response.status_code == 200:
#     comments = comments_response.json()
#     print("Доступные комментарии:")
#     for comment in comments['comments']:
#         print(f"  ID: {comment['id']} - '{comment['text'][:50]}...' (Статья ID: {comment['article_id']})")

# update_comment_data = {
#     "text": "Этот комментарий был ОТРЕДАКТИРОВАН с API"
# }

# comment_id = 1
# response = session.put(
#     f"http://127.0.0.1:5000/api/comment/{comment_id}",
#     json=update_comment_data
# )

# print(f"\nРезультат редактирования комментария ID {comment_id}:")
# print(f"Статус: {response.status_code}")
# print(f"Ответ: {response.json()}")
# print(f"Текст ответа: {response.text[:200]}")

# #УДАЛЕНИЕ КОММЕНТА
# import requests

# session = requests.Session()

# login_data = {
#     'email': 'mrdmitry2006@mail.ru',
#     'password': '123456'
# }
# login_response = session.post('http://127.0.0.1:5000/login', data=login_data)
# print(f"Авторизация: {login_response.status_code}")


# comments_response = session.get("http://127.0.0.1:5000/api/comment")
# if comments_response.status_code == 200:
#     comments = comments_response.json()
#     print("Доступные комментарии:")
#     for comment in comments['comments']:
#         print(f"  ID: {comment['id']} - '{comment['text'][:50]}...' (Статья ID: {comment['article_id']}, Автор: {comment['author_name']})")


# comment_id = 1
# response = session.delete(
#     f"http://127.0.0.1:5000/api/comment/{comment_id}"
# )

# print(f"\n Результат удаления комментария ID {comment_id}:")
# print(f"Статус: {response.status_code}")
# print(f"Ответ: {response.json()}")

# #GET 
# import requests

# res = requests.get("http://127.0.0.1:5000/api/articles/sort/date")
# print(res.json())  
# 
# http://127.0.0.1:5000/api/articles/category/Технологии
#  