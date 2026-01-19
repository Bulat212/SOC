from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True)
class AddUserDTO:
    telegram_id: str
    username: str | None = field(default=None)
    first_name: str | None = field(default=None)
    last_name: str | None = field(default=None)
    role: str


@dataclass(slots=True, kw_only=True)
class GetUserDTO:
    id: str
    telegram_id: str
    username: str | None = field(default=None)
    first_name: str | None = field(default=None)
    last_name: str | None = field(default=None)
    role: str
    is_active: bool


@dataclass(slots=True)
class GetUserIDDTO:
    id: str | None = field(default=None)
    telegram_id: str | None = field(default=None)

    def __post_init__(self) -> None:
        if not self.id and not self.telegram_id:
            raise AttributeError()
        elif self.id and self.telegram_id:
            raise AttributeError()


@dataclass(slots=True)
class GetUsersIDDTO:
    values: list[GetUserIDDTO]
