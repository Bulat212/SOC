from dataclasses import dataclass, field
import datetime


@dataclass(slots=True, kw_only=True)
class Delegate:
    id: str | None = field(default=None)
    user_id: str
    telegram_id: str
    first_name: str | None
    last_name: str | None
    patronymic: str | None
    post: str | None
    subject: str | None
    start_date: datetime.date | None
    end_date: datetime.date | None




