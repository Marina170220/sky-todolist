#Todolist (Final project)

###Привет!
###Это итоговый проект курса Python-разработчик от SkyPro.

Целью данного проекта является создание веб-приложения — планировщика задач.

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


step#1:

Подготовка проекта и настройка необходимых системных компонентов для дальнейшей работы.

step#2:

Настройка локальной разработки с помощью Docker Compose и автоматического деплоя всего приложения на сервер по пушу в GitHub.

step#3:

Реализация методов API, описанных в документации swagger. Аутентификация и авторизация. Авторизация через VK с помощью OAuth2.0.

step#4:

Добавлена возможность добавления категорий, целей и комментариев к ним. Сортировка целей по дате дедлайна и приоритету.

step#5:

Добавлены доски с целями и возможность шеринга досок между участниками.