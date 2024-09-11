# foodgram
foodgram

## Описание

Проект представляет собой сайт для размещения рецептов
Возможности:
- создание рецептов
- подписка на другого пользователя
- добавление рецептов в избранное
- добавление рецептов в корзину
- формирование списка покупок в формате excel

## Необходимые данные
- url проекта https://foodgram-kafes.sytes.net/
- данные админа: логин admin@example.com, пароль securepassword

## Как запустить проект

1. Перейдите в директорию infra
2. Запустите Docker
3. Выполните команду docker compose up
4. Примените миграции docker compose exec backend python manage.py migrate 
5. выполните следующие команды:
   - docker compose exec backend python manage.py create_superuser --username admin --email admin@example.com --password securepassword --first_name Admin --last_name Admin
   - docker compose exec backend python manage.py load_ingredients_json 
   - docker compose exec backend python manage.py load_tags_json

## Технологии

Бэкенд выполнен на базе Django
Запуск осуществляется с помощью Docker

## Авторы

Бэкенд - Феськов Константин
Развёртывание в Docker - Феськов Константин
Фронтенд - Yandex team