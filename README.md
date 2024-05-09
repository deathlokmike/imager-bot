# Телеграм-бот для создания скриншотов веб-страниц

## Cтек

- Фреймворк: **py-telegram-bot**

- БД: **PostgreSQL**

- ORM: **SQLAlchemy**

## Запуск 
Скопируйте .env_example в .env и отредактируйте .env файл, заполнив в нём все переменные окружения:
  ```bash
  cp .env_example .env
  ```
### Тестовый вариант
Для запуска приложения вам потребуется Docker и poetry. Вы можете запустить приложение локально, для этого понадобится:
- Установите зависимости:
    ```bash
    poetry install
    ```  
- Активируйте виртуальное окружение:
    ```bash
    poetry shell
    ```  
- Установите MODE .env в TEST или DEV
- Запустите БД:
    ```bash
    docker compose -f compose_tests.yaml up
    ```  
- Заполните БД необходимыми данными: 
  ```bash
  alembic upgrade head && python imager_bot/init_db.py
  ```
- Запустите бота
    ```bash
    python imager_bot/main.py
    ```  
### Деплой
Для запуска приложения в продакшн вам потребуется:
- Установите MODE .env в PROD
- Соберите проект:
    ```bash
   docker compose -f compose_prod.yaml build
    ```  
- После успешной сборки можно поднять контейнер:
    ```bash
   docker compose -f compose_prod.yaml up
    ```  

