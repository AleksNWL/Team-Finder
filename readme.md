# TeamFinder

Веб-приложение для поиска команды под pet-проекты. Реализован **вариант 1**: избранное и фильтрация пользователей (`TASK_VERSION=1`).

## Запуск для ревьюера (Docker Compose)

1. Скопируйте `.env_example` в `.env` и при необходимости измените секреты.
2. В корне проекта выполните:

```bash
docker compose up --build
```

3. Откройте в браузере: http://127.0.0.1:8000/

При старте контейнера `web` автоматически выполняются миграции и команда `seed_demo` (демо-пользователи и проекты).

Данные PostgreSQL и загруженные медиафайлы сохраняются в Docker volumes (`postgres_data`, `media_data`).

## Демо-аккаунты

| Роль | Email | Пароль |
|------|-------|--------|
| Пользователь | anna@demo.team | demo12345 |
| Пользователь | boris@demo.team | demo12345 |
| Пользователь | clara@demo.team | demo12345 |
| Администратор | admin@demo.team | admin12345 |

У каждого демо-пользователя есть хотя бы один проект. Между аккаунтами настроены избранное и участие в проектах для проверки фильтров на `/users/list/`.

## Админ-панель

http://127.0.0.1:8000/admin/ — вход под `admin@demo.team` / `admin12345`.

## Локальный запуск без Docker

1. Установите PostgreSQL и создайте БД из `.env`.
2. `python -m venv venv` → активация → `pip install -r requirements.txt`
3. `python manage.py migrate`
4. `python manage.py seed_demo`
5. `python manage.py runserver`

В `.env` укажите `POSTGRES_HOST=localhost` и `TASK_VERSION=1`.

## Основные URL

| Страница | URL |
|----------|-----|
| Главная (проекты) | `/projects/list/` |
| Избранное | `/projects/favorites/` |
| Участники | `/users/list/` |
| Регистрация | `/users/register/` |
| Вход | `/users/login/` |
