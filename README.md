# Задание:
Реализовать простую реферальную систему. Минимальный интерфейс для тестирования.

# Реализовать логику и API для следующего функционала:
-   Авторизация по номеру телефона. 
    -   Первый запрос на ввод номера телефона. ✅
    -   Имитировать отправку 4хзначного кода авторизации(задержку на сервере 1-2 сек). ✅
    -   Второй запрос на ввод кода ✅
-   Если пользователь ранее не авторизовывался, то записать его в бд ✅
-   Запрос на профиль пользователя ✅
-   Пользователю нужно при первой авторизации нужно присвоить рандомно сгенерированный 6-значный инвайт-код(цифры и символы) ✅
-   В профиле у пользователя должно быть:
    -   возможность ввести чужой инвайт-код(при вводе проверять на существование). ✅
    -   В своем профиле можно активировать только 1 инвайт код. ✅
    -   если пользователь уже когда-то активировал инвайт код, то нужно выводить его в соответсвующем поле в запросе на профиль пользователя. ✅
-   В API профиля должен выводиться список пользователей(номеров телефона), которые ввели инвайт код текущего пользователя. ✅
-   Реализовать и описать в readme Api для всего функционала ✅
-   Создать и прислать Postman коллекцию со всеми запросами ✅
-   Залить в сеть, чтобы удобнее было тестировать(залью на свой сервер) ✅

## Опционально:
-   Интерфейс на Django Templates ❌
-   Документирование апи при помощи ReDoc ✅
-   Docker ✅

## Ограничения на стек технологий:
-   Python ✅
-   Django, DRF ✅
-   PostgreSQL ✅
-   Дополнительно:
    - CI/CD ✅
    - Nginx (для обслуживания статики (админ панель и документация swagger/redoc)) ✅
    - Redis (добавлен для демонстрации, хотя кэшировать особо нечего) ✅

### Для более детальной информации о структуре проекта и API смотрите [docs.md](docs.md).

