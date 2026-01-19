import os
import tomllib
from dataclasses import dataclass
from typing import Any

from app.exceptions import ConfigException


@dataclass(slots=True)
class S3Config:
    endpoint: str
    access_key: str
    secret_key: str
    verify: bool
    promo_bucket: str
    candidate_bucket: str


@dataclass(slots=True)
class TemplateConfig:
    candidate_bucket: str
    candidate_name_template: str


@dataclass(slots=True)
class BrokerConfig:
    url: str


@dataclass(slots=True)
class DatabaseConfig:
    url: str


@dataclass(slots=True)
class ApplicationConfig:
    database: DatabaseConfig
    broker: BrokerConfig
    s3: S3Config
    template: TemplateConfig


def _get_path_config() -> str:
    key = "BASE_CONFIG"
    if (path := os.getenv(key)) is None:
        raise ConfigException(key)
    return path


def _get_config(path: str) -> dict[str, Any]:
    with open(path, mode="rb") as file:
        return tomllib.load(file)


def load_config():
    path_config = _get_path_config()
    data = _get_config(path_config)
    return ApplicationConfig(
        database=DatabaseConfig(
            **data["database"],
        ),
        broker=BrokerConfig(
            **data["broker"],
        ),
        s3=S3Config(
            **data["s3"],
        ),
        template=TemplateConfig(
            **data["template"],
        ),
    )
