from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True)
class User:
    id: str | None = field(default=None)
    telegram_id: str
    username: str | None = field(default=None)
    first_name: str | None = field(default=None)
    last_name: str | None = field(default=None)
    full_name: str | None = field(default=None)
    role: str
    is_active: bool

    def __post_init__(self) -> None:
        self.full_name = (
                self.full_name or f"{self.first_name} {self.last_name}"
        )
