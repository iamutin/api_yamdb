# api_yamdb

## Стек технологий
[![Python](https://img.shields.io/badge/Python-3.9-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-3.2-blue?style=for-the-badge&logo=django)](https://www.djangoproject.com/)
[![REST_FRAMEWORK](https://img.shields.io/badge/Django_REST_framework-3.12-blue?style=for-the-badge&logo=django)](https://www.django-rest-framework.org/)

## Как запустить проект

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:iamutin/api_yamdb.git
```

```
cd api_yamdb
```

Создать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv\Scripts\activate
```

Обновить менеджер пакетов pip

```
python -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Создать в директории **api_yamdb** файл **.env** и добавить в него следующие строки:
```
DEBUG=<True или False>
SECRET_KEY=<секретный ключ для django-приложения>
ALLOWED_HOSTS=<перечислить адреса через пробел>
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

## Документация
Документация в формате ReDoc будет доступа после запуска проекта по адресу:

http://127.0.0.1:8000/redoc/
