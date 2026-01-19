import datetime
from pydantic import Field

from app.presentation.schema.base import Base


class GetDelegateIDSchema(Base):
    telegram_id: str | None = Field(None)


class GetDelegateSchema(Base):
    id: str = Field(...)
    telegram_id: str = Field(...)
    user_id: str = Field(...)
    first_name: str | None = Field(...)
    last_name: str | None = Field(...)
    patronymic: str | None = Field(...)
    post: str | None = Field(...)
    subject: str | None = Field(...)
    start_date: datetime.date | None = Field(...)
    end_date: datetime.date | None = Field(...)


class UpdateDelegateSchema(Base):
    id: str | None = Field(None)
    telegram_id: str | None = Field(None)
    user_id: str | None = Field(None)
    first_name: str | None = Field(...)
    last_name: str | None = Field(...)
    patronymic: str | None = Field(...)
    post: str | None = Field(...)
    subject: str | None = Field(...)
    start_date: datetime.date | None = Field(...)
    end_date: datetime.date | None = Field(...)


class AddDelegateSchema(Base):
    telegram_id: str
    user_id: str
    first_name: str
    last_name: str
    patronymic: str
    post: str
    subject: str | None = Field(...)
    start_date: datetime.date | None = Field(...)
    end_date: datetime.date | None = Field(...)