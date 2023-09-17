# API сервис для менеджмента заметок

Rest APIs:
- CRUD Notes
- CRUD Board

Использовано:
- Python
- FastAPI
- asyncio
- Postgres
- REST API



## Installation


Создайте пустую БД ***notes_db*** для **PostgreSQL**.

Выполните установку необходимых библиотек:
```bash
    pip install requirements.txt
```

Создайте таблицы с помощью миграций выполнив команду
```bash
    alembic upgrade head
```

Запустите сервер
```bash
    uvicorn main:app --reload
```

Если нужно заполнить БД тестовыми данными, то запустите скрипт **note_app/scripts/gener_data.py**.
## Ошибки

### Проверьте конфигурации для соединения с БД. При необходимости установите свои параметры:

### В файле note_app/database.py
```python
postgresql+asyncpg://postgres:admin@127.0.0.1:5432/notes_db

postgresql+asyncpg://{user_db}:{password}@{host}:{port}/{name_db}
```
### Тоже самое в файле alembic.ini
```python
sqlalchemy.url = postgresql://postgres:admin@127.0.0.1:5432/notes_db
```
