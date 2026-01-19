from pydantic import Field

from app.presentation.schema.base import Base


class AddFaqIDSchema(Base):
    id: str = Field(...)


class GetFaqSchema(Base):
    id: str = Field(...)
    question: str = Field(...)
    answer: str = Field(...)


class GetFaqListSchema(Base):
    total: int = Field(...)
    limit: int = Field(...)
    offset: int = Field(...)
    values: list[GetFaqSchema] = Field(...)


class AddFaqSchema(Base):
    question: str = Field(...)
    answer: str = Field(...)
