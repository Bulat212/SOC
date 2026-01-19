from pydantic import Field

from .base import Base


class GetAboutUsSchema(Base):
    text: str = Field(...)
