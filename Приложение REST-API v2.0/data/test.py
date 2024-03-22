from requests import get, delete, post
import datetime

# Правильный запрос
print(get('http://localhost:5000/api/v2/users').json())

# Неправильное название
print(get('http://localhost:5000/api/v2/user').json())

# Правильный запрос
print(get('http://localhost:5000/api/v2/users/1').json())

# Не существует пользователя с таким айди
print(get('http://localhost:5000/api/v2/users/912931293219').json())

# Строка вместо айди
print(get('http://localhost:5000/api/v2/users/s').json())

# Пустой запрос
print(get('http://localhost:5000/api/v2/users/').json())

# Правильно добавили пользователя
print(post('http://localhost:5000/api/v2/users',
           json={'surname': '2',
                 'name': 'Название работы',
                 'age': '1',
                 'position': '12',
                 'speciality': '21.03.2024',
                 'address': '~',
                 'email': '3@3'}).json())

# В age только целочисленный тип данных
print(post('http://localhost:5000/api/v2/users',
           json={'surname': '2',
                 'name': 'Название работы',
                 'age': 'z1',
                 'position': '12',
                 'speciality': '21.03.2024',
                 'address': '~',
                 'email': '1@1'}).json())

# Неправильный ключ
print(post('http://localhost:5000/api/v2/users',
           json={'surnamez': '2',
                 'name': 'Название работы',
                 'age': '1',
                 'position': '12',
                 'speciality': '21.03.2024',
                 'address': '~',
                 'email': '1@1'}).json())

# Отсутствует нужный ключ
print(post('http://localhost:5000/api/v2/users',
           json={'name': 'Название работы',
                 'age': '1',
                 'position': '12',
                 'speciality': '21.03.2024',
                 'address': '~',
                 'email': '1@1'}).json())
# Удалили пользователя
print(delete('http://localhost:5000/api/v2/users/1').json())

# Нет работы с таким индексом
print(delete('http://localhost:5000/api/v2/users/123123123123123').json())

# Строка вместо айди
print(delete('http://localhost:5000/api/v2/users/ф').json())

# Пустой запрос
print(delete('http://localhost:5000/api/v2/users/').json())
