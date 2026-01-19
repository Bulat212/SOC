from pydantic import Field

from .base import Base


class AddQuestionSchema(Base):
    user_id: str | None = Field(None)
    telegram_id: str | None = Field(None)
    question: str = Field(...)


class GetQuestionSchema(Base):
    id: str = Field(...)
    user_id: str | None = Field(None)
    number: int | None = Field(None)
    question: str = Field(...)
    is_answer: bool = Field(...)


class AddQuestionIDSchema(Base):
    question_id: str = Field(...)


class GetQuestionListSchema(Base):
    total: int = Field(...)
    limit: int = Field(...)
    offset: int = Field(...)
    values: list[GetQuestionSchema] = Field(...)
