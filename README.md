# rest-api-using-django-with-tdd
### Recipes api
[![Build Status](https://travis-ci.org/Zed-chi/Recipes-rest-api-using-django-with-tdd.svg?branch=master)](https://travis-ci.org/Zed-chi/Recipes-rest-api-using-django-with-tdd)

Нужно изменять IPдля доступа в приложение
28строка  файла app/app/settings.py

Точка входа в recipe
http://localhost:5000/api/recipe/
http://localhost:5000/api/recipe/tags/
http://localhost:5000/api/recipe/ingredients/
http://localhost:5000/api/recipe/recipes/

Точка входа в user
http://localhost:5000/api/user/
страницы нет, но есть вывод по api командам аутентификации
api/user/ create/ [name='create']
api/user/ token/ [name='token']
api/user/ me/ [name='me']
api/recipe/
^media/(?P<path>.*)$

Точка логина в django
http://localhost:5000/admin/

Запуск и первичная сборка.
docker-compose up
Пересборка если есть изменения
docker-compose build
Остановка
CTRL+C
И возможно
docker-compose down

project from https://www.udemy.com/course/django-python-advanced
