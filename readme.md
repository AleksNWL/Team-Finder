# TeamFinder

Платформа для поиска команды под pet-проекты: пользователи публикуют идеи, просматривают проекты других участников, добавляют понравившиеся в избранное и присоединяются к командам.

## Возможности

- регистрация и вход по email;
- лента проектов с пагинацией и карточками;
- избранное и фильтрация участников (вариант 1);
- профили с контактами, создание и редактирование проектов;
- участие в чужих проектах и управление своими;
- админ-панель Django.

## Стек

- Python 3.12
- Django 5.2
- PostgreSQL 16
- Pillow
- Docker, Docker Compose

## Переменные окружения

Скопируйте `.env_example` в `.env`:

| Переменная | Назначение |
|------------|------------|
| `DJANGO_SECRET_KEY` | секретный ключ Django |
| `DJANGO_DEBUG` | режим отладки (`True` / `False`) |
| `DJANGO_ALLOWED_HOSTS` | разрешённые хосты через запятую |
| `POSTGRES_DB` | имя базы данных |
| `POSTGRES_USER` | пользователь PostgreSQL |
| `POSTGRES_PASSWORD` | пароль PostgreSQL |
| `POSTGRES_HOST` | хост БД (`db` в Docker, `localhost` локально) |
| `POSTGRES_PORT` | порт PostgreSQL |

## Запуск (Docker Compose)

```bash
docker compose up --build
```

Сайт: http://127.0.0.1:8000/

При старте выполняются миграции и `seed_demo`. Данные хранятся в volumes `postgres_data` и `media_data`.

### Демо-аккаунты

| Роль | Email | Пароль |
|------|-------|--------|
| Пользователь | anna@demo.team | demo12345 |
| Пользователь | boris@demo.team | demo12345 |
| Пользователь | clara@demo.team | demo12345 |
| Администратор | admin@demo.team | admin12345 |

Админ-панель: http://127.0.0.1:8000/admin/

## Локальный запуск

1. PostgreSQL и база по параметрам из `.env`.
2. `python -m venv venv` → активация → `pip install -r requirements.txt`
3. `python manage.py migrate`
4. `python manage.py seed_demo`
5. `python manage.py runserver`

В `.env` для локального запуска укажите `POSTGRES_HOST=localhost`.

## Автор

- Имя: Алексей
- GitHub: [https://github.com/AleksNWL](https://github.com/AleksNWL)
- Email: Grifon595@yandex.ru
