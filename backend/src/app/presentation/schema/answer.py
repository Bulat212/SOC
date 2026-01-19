from pydantic import Field

from .base import Base


class AddAnswerSchema(Base):
    question_id: str = Field(...)
    answer: str = Field(...)


class GetAnswerSchema(Base):
    question_id: str = Field(...)
    answer: str = Field(...)
