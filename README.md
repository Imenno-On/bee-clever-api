# Bee Clever

## Описание
Bee Clever — приложение-аггрегатор для подбора онлайн-курсов. 
## Stack
- Python
- Django REST
- Docker
- PostgreSQL

## Требования
- Python 3.x
- Docker

## Установка

1. Склонируйте репозиторий
    
2. Запустите Docker Engine

3. Постройте Docker контейнер с помощью команды:
    ```bash
    docker-compose build
    ```

## Запуск Проекта

1. Примените необходимые миграции:
    ```bash
    docker-compose run --rm app sh -c "python manage.py migrate"
    ```

2. Запустите сервер:
    ```bash
    docker-compose up
    ```

Приложение должно быть готово к работе.

## Запуск Тестов
Чтобы запустить тесты, воспользуйтесь следующей командой:
```bash
docker-compose run --rm app sh -c "python manage.py test"
```
