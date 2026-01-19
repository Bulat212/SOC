from dataclasses import dataclass


@dataclass(slots=True)
class GetUserDTO:
    id: str
    telegram_id: str
    username: str | None
    first_name: str | None
    last_name: str | None
    full_name: str | None
    role: str
    is_active: bool


@dataclass(slots=True)
class UserIDDTO:
    telegram_id: str


@dataclass(slots=True)
class GetUserIDDTO:
    telegram_id: str


@dataclass(slots=True)
class GetUsersIDDTO:
    values: list[GetUserIDDTO]
