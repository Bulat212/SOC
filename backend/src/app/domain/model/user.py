from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True)
class User:
    id: str | None = field(default=None)
    telegram_id: str
    username: str | None = field(default=None)
    first_name: str | None = field(default=None)
    last_name: str | None = field(default=None)
    role_id: str
    is_active: bool = field(default=True)
