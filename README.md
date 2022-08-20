#Todolist (Final project)

###Привет!
###Это итоговый проект курса Python-разработчик от SkyPro.

Целью данного проекта является создание веб-приложения — планировщика задач.
Проект размещен на домене sky-todolist.ga

Cтек:
  - python 3.10,
  - Django 4.0.1,
  - Postgres 12.4

Для запуска проекта клонируйте репозиторий и установите зависимости:

pip install -r requirements.txt

Создайте в корне проекта файл .env и укажите значения констант:
- DEBUG
- DATABASE_URL
- SECRET_KEY
- SOCIAL_AUTH_VK_OAUTH2_KEY
- SOCIAL_AUTH_VK_OAUTH2_SECRET
- BOT_TOKEN

Чтобы запустить приложение воспользуйтесь командой docker-compose up -d

###Этапы выполнения работы:

step#1:

Подготовка проекта и настройка необходимых системных компонентов для дальнейшей работы.

step#2:

Настройка локальной разработки с помощью Docker Compose и автоматического деплоя всего приложения на сервер по пушу в GitHub.

step#3:

Реализованы методы API, описанных в документации swagger. Аутентификация и авторизация. Авторизация через VK с помощью OAuth2.0.

step#4:

Реализована возможность добавления категорий, целей и комментариев к ним. Сортировка целей по дате дедлайна и приоритету.

step#5:

Добавлены доски с целями и возможность шеринга досок между участниками.

step#6:

Добавлен телеграм-бот. Просмотреть свои цели и запланировать новые можно с помощью бота: @sky_todolist_bot