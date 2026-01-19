from dataclasses import dataclass
import datetime


@dataclass(kw_only=True, slots=True)
class DelegateIDDTO:
    telegram_id: str


@dataclass(kw_only=True, slots=True)
class GetDelegateDTO:
    id: str
    telegram_id: str 
    user_id: str
    first_name: str | None
    last_name: str | None
    patronymic: str | None
    post: str | None
    subject: str | None
    start_date: datetime.date | None
    end_date: datetime.date | None


@dataclass(kw_only=True, slots=True)
class UpdateDelegateDTO:
    telegram_id: str | None
    first_name: str | None
    last_name: str | None
    patronymic: str | None
    post: str | None
    subject: str | None
    start_date: datetime.date | None
    end_date: datetime.date | None


@dataclass(kw_only=True, slots=True)
class GetDelegateDTO:
    id: str
    telegram_id: str 
    user_id: str
    first_name: str | None
    last_name: str | None
    patronymic: str | None
    post: str | None
    subject: str | None
    start_date: datetime.date | None
    end_date: datetime.date | None


@dataclass(kw_only=True, slots=True)
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
