from dataclasses import dataclass, field
import datetime


@dataclass(slots=True, kw_only=True)
class GetDelegateIDDTO:
    telegram_id: str

@dataclass(slots=True, kw_only=True)
class GetDelegateDTO:
    id: str
    telegram_id: str
    user_id: str
    first_name: str | None = field(default=None)
    last_name: str | None = field(default=None)
    patronymic: str | None = field(default=None)
    post: str | None = field(default=None)
    subject: str | None = field(default=None)
    start_date: datetime.date | None = field(default=None)
    end_date: datetime.date | None = field(default=None)


@dataclass(slots=True, kw_only=True)
class UpdateDelegateDTO:
    id: str | None
    telegram_id: str | None
    user_id: str | None
    first_name: str | None
    last_name: str | None
    patronymic: str | None
    post: str | None
    subject: str | None
    start_date: datetime.date | None
    end_date: datetime.date | None


@dataclass(slots=True, kw_only=True)
class AddDelegateDTO:
    telegram_id: str
    user_id: str
    first_name: str
    last_name: str
    patronymic: str
    post: str
    subject: str | None
    start_date: datetime.date | None
    end_date: datetime.date | None