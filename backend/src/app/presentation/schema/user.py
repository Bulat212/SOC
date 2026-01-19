from pydantic import Field

from app.presentation.schema.base import Base


class AddUserSchema(Base):
    telegram_id: str = Field(...)
    username: str | None = Field(...)
    first_name: str | None = Field(...)
    last_name: str | None = Field(...)


class GetUserSchema(Base):
    id: str = Field(...)
    telegram_id: str = Field(...)
    username: str | None = Field(...)
    first_name: str | None = Field(...)
    last_name: str | None = Field(...)
    role: str = Field(...)
    is_active: bool = Field(...)


class GetUserIDSchema(Base):
    id: str | None = Field(None)
    telegram_id: str | None = Field(None)


class GetUsersIDSchema(Base):
    values: list[GetUserIDSchema] = Field(...)

class DeleteUserSchema(Base):
    user_id: str = Field(...)