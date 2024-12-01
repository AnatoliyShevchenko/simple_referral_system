
# Docs
Сервис развернут на облачной машине и доступен для тестирования. Для взаимодействия с API доступны интерактивные документации:
- http://77.246.247.217/redoc/
- http://77.246.247.217/swagger/

В репозитории предоставлены:
- коллекции Postman (окружение, запросы)
- .env_example если есть желание запустить сервис у себя

Все переменные окружения переданы в репозиторий через секреты репозитория. Генерация .env файла происходит в процессе деплоя.
Сервис запущен с использованием gunicorn, а обработка статики осуществляется через Nginx (SSL-сертификаты не подключены).

---
## Структура проекта
```plaintext
├── .github/                # Конфигурации для CI/CD
│   └── workflows/
│       └── main.yml        # Основной pipeline для деплоя
│
├── apps/                   # Основные приложения
│   └── auths/              # Приложение для авторизации и управления профилем
│       ├── migrations/     # Миграции базы данных
│       ├── admin.py        # Регистрация моделей в Django Admin
│       ├── apps.py         # Конфигурация приложения
│       ├── models.py       # Определение моделей базы данных
│       ├── serializers.py  # DRF сериализаторы
│       ├── tests.py        # Тесты авторизации
│       └── views.py        # Основная логика API (авторизация, профиль)
│
├── scripts/                # Скрипты для управления проектом
│   ├── wait-for.sh         # Ожидание доступности базы данных перед стартом
│   └── entrypoint.sh       # Основной скрипт для запуска приложения (миграции, сбор статики)
│
├── settings/               # Настройки проекта
│   ├── asgi.py             # Запуск в асинхронном режиме (Uvicorn/Daphne)
│   ├── base.py             # Основные настройки проекта
│   ├── urls.py             # Регистрация URL маршрутов
│   └── wsgi.py             # Запуск в синхронном режиме (Gunicorn)
│
├── .env_example            # Шаблон файла переменных окружения
├── Dockerfile              # Инструкция для сборки Docker-образа
├── docker-compose.yml      # Конфигурация для запуска зависимостей
├── manage.py               # Основной файл для управления проектом
├── requirements.txt        # Список Python-зависимостей
└── nginx.conf              # Конфигурация Nginx
```
---
## Таблица методов для взаимодействия:
| Метод  | Эндпоинт                | Описание                          |
|--------|-------------------------|-----------------------------------|
| POST   | /api/v1/auth/           | Авторизация по номеру телефона    |
| PATCH  | /api/v1/auth/           | Проверка кода авторизации         |
| GET    | /api/v1/user/           | Получение профиля                 |
| PATCH  | /api/v1/user/           | Ввод кода приглашения             |

---
## Примеры взаимодействия:
> **Авторизация по номеру телефона** 
*Метод:* `POST`  
*Эндпоинт:* `/api/v1/auth/` 

##### Request:
```
{
    "phone_number":"+77777777777"
}
```
##### Response:
-   200 OK
    ```
    {
        "message": "Your authenticate code has been sent to your phone! (9405) It's active only for 2 minutes!"
    }
    ```
-   400 Bad Request(корректность номера проверяется регулярным выражением):
    ```
    {
        "detail": "Invalid input."
    }
    ```
---
> **Ввод кода подтверждения**
*Метод:* `PATCH`  
*Эндпоинт:* `/api/v1/auth/`

##### Request:
```
{
    "auth_code":"1735"
}
```
##### Response:
-   200 OK
    ```
    {
        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMzEyNTk0NCwiaWF0IjoxNzMzMDM5NTQ0LCJqdGkiOiJkNTU2NWU2YjJiMTQ0YTM5ODAxZmZmNDBjZjZmZDRjZCIsInVzZXJfaWQiOjJ9.65SNI5mB9pPIPK7ppUIgwR5Wf6346NUapuyei10cEYk",
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMzMDM5ODQ0LCJpYXQiOjE3MzMwMzk1NDQsImp0aSI6ImE4ZTc1ZTg0MmM1ZTRmNzk4N2YwOTNkOTRiYmI3MjhiIiwidXNlcl9pZCI6Mn0.OG0W4c5mgIKoHtdeFdSQBfa-8hijLZA2pyw7xDjCzdQ"
    }
    ```
-   404 Not Found(срок действия кода 2 минуты, либо просрочен, либо не найден):
    ```
    {
        "detail": "Auth code is invalid or expired"
    }
    ```
---
> **Профиль пользователя**
*Метод:* `GET`  
*Эндпоинт:* `/api/v1/user/`

##### Request: 
-   empty
##### Headers:
-   Authorization: Bearer {{ACCESS_TOKEN}}

##### Response:
-   200 OK
    ```
    {
        "phone": "+77777777777",
        "invite_code": "vzalS2",
        "inviter": null,
        "invited_users": [
            {
                "invite_code": "GXwcSK",
                "phone": "+77777777776"
            },
            {
                "invite_code": "XJXBiJ",
                "phone": "+77777777775"
            }
        ]
    }
    ```
---
> **Ввод кода приглашения**
*Метод:* `PATCH`  
*Эндпоинт:* `/api/v1/user/`

##### Request: 
```
{
    "invited_by":"vzalS2"
}
```
##### Headers:
-   Authorization: Bearer {{ACCESS_TOKEN}}
##### Response:
-   200 OK
    ```
    {
        "detail": "You have successfully activated the invite code!"
    }
    ```
-   404 Not Found
    ```
    {
        "detail": "user not found"
    }
    ```
-   409 Conflict:
    ```
    {
        "detail": "you have already activate the code!"
    }
    ```
---