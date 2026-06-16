import os
import tomllib
from dataclasses import dataclass
from typing import Any

from bot.exceptions import ConfigException


@dataclass(slots=True)
class BrokerConfig:
    url: str


@dataclass(slots=True)
class RedisConfig:
    url: str


@dataclass(slots=True)
class BotConfig:
    telegram_api_url: str
    sticker_id: str
    token: str
    group_id: int | None
    questions_topic_id: int | None
    new_registration_topic_id: int | None
    channel_id: str
    broker: BrokerConfig
    redis: RedisConfig
    yandex_form_url: str


def _get_config_path():
    key = "BASE_CONFIG"
    if (path := os.getenv(key)) is None:
        raise ConfigException(key)
    return path


def _get_config(path: str) -> dict[str, Any]:
    with open(path, mode="rb") as file:
        return tomllib.load(file)


def load_config() -> BotConfig:
    path_config = _get_config_path()
    data = _get_config(path_config)

    return BotConfig(
        token=data["bot"]["token"],
        sticker_id=data["bot"]["sticker_id"],
        telegram_api_url=data["bot"]["telegram_api_url"],
        group_id=data["bot"].get("group_id"),
        questions_topic_id=data["bot"].get("questions_topic_id"),
        new_registration_topic_id=data["bot"].get("new_registration_topic_id"),
        channel_id=data["bot"].get("channel_id"),
        yandex_form_url=data["bot"].get("yandex_form_url"),
        broker=BrokerConfig(
            **data["broker"],
        ),
        redis=RedisConfig(
            **data["redis"],
        ),
    )
