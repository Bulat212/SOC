# Сервис взаимодействия с кандидатом

### Запуск сервис локально

1. Установить [uv](https://docs.astral.sh/uv/getting-started/installation/)

2. Синхронизировать зависимости: `uv sync`

3. Создать [config.toml](./config/example.config.toml)

4. Указать в переменных окружения параметр `BASE_CONFIG` и путь до файла конфигураций:

    * Windows: `$env:BASE_CONFIG="<PATH>/config/config.toml"`

    * Linux: `export BASE_CONFIG="<PATH>/config/config.toml"`

5. Запустить сервис с брокером сообщений: `uv run faststream run --factory app.main:get_faststream_app` (для запуска во время
   разработки используйте флаг `--reload`)


### Запуск сервиса в контейнере

1. Установить [Docker](https://docs.docker.com/engine/install/)

2. Создать образ: `docker build -t backend`

3. Запустить контейнер: `docker run backend:v1`
