from pydantic import Field

from .base import Base


class GetTelegramChannelSchema(Base):
    channel: str = Field(...)
