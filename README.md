# Чат-бот для помощи группе отбора кандидатов

### Сервисы

Проект состоит из двух сервисов: [backend](./backend/README.md) и [bot](./bot/README.md). Взаимодействие между ними
реализовано с помощью брокера сообщения `RabbitMQ`.

### Технологии

|     Python     |    RabbitMQ    |      Alembic       | PostgreSQL |
|:--------------:|:--------------:|:------------------:|:----------:|
| **FastStream** | **SQLAlchemy** |    **aiogram**     | **Docker** |
|   **dishka**   |  **alembic**   | **aiogram-dialog** | **MinIO**  |

### Licence

[Apache](./LICENSE)
