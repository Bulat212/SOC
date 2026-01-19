from pydantic import Field

from .base import Base


class GetInfoSchema(Base):
    id: str = Field(...)
    about_us_url: str | None = Field(...)
    telegram_channel_url: str | None = Field(...)
    is_info: bool = Field(...)
