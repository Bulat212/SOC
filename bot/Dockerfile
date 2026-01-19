FROM python:3.13.2 AS build

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

ADD https://astral.sh/uv/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh

FROM build AS bot

ENV PATH="/root/.local/bin/:$PATH"
ENV UV_LINK_MODE=copy

ADD . ./app

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

CMD ["uv", "run", "python", "-m", "bot"]
