# python-messenger-api
Api для мессенджера, позволяющий получать данные пользователя,
его сообщения и чаты.



## Локальное окружение
С помощью docker-compose запускаются следующие контейнеры:
- `postgres` - СУБД, хранящая основные сущности.
- `redis` - NoSQL СУБД. Хранит данные в виде ключ-значение. Используется
как брокер сообщений.
- `flower` - мониторинг **celery** кластеров.

___

## Uvicorn
**Uvicorn** - это реализация веб-сервера ASGI для Python.

###Запуск веб-приложения на localhost:8080

`.\venv\Scripts\python.exe -m uvicorn main:app --reload --port 8080`

___

## Celery
**Celery** - это очередь задач. Он получает задания из нашего приложения 
и запускает их в фоновом режиме. 
Celery должен быть сопряжен с другими сервисами, которые действуют в качестве брокеров.

___

## Alembic
**Alembic** - инструмент, использующий SQLAlchemy в качестве движка,
для управления базой данных как на уровне SQL запросов,
так и с помощью сценариев.

###Генерация изменений
`.\venv\Scripts\python.exe -m alembic revision -m "init" --autogenerate`

### Применение ревизий
`.\venv\Scripts\python.exe -m alembic upgrade head`

### Откат одной ревизии
`.\venv\Scripts\python.exe -m alembic downgrade -1`

