from dataclasses import dataclass, field
import datetime


@dataclass(slots=True, kw_only=True)
class Delegate:
    id: str | None = field(default=None)
    user_id: str
    telegram_id: str
    first_name: str | None = field(default=None)
    last_name: str | None = field(default=None)
    patronymic: str | None = field(default=None)
    post: str | None = field(default=None)
    subject: str | None = field(default=None)
    start_date: datetime.date | None = field(default=None)
    end_date: datetime.date | None = field(default=None)