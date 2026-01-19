import datetime
from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True)
class Candidate:
    id: str | None = field(default=None)
    telegram_id: str | None = field(default=None)
    recruitment_id: str
    nationality: str
    first_name: str
    last_name: str
    patronymic: str
    birthdate: datetime.date
    subject: str
    military_station: str
    military_station_address: str
    university: str
    graduation_date: datetime.date
    direction_training: str
    average_score: float
    find_out: str
    phone_number: str
    is_form: bool = field(default=False)
    is_statement: bool = field(default=False)
    is_approval: bool = field(default=False)


@dataclass(slots=True, kw_only=True)
class CandidateQuote:
    id: str | None = field(default=None)
    total: int
    count: int
    approved: int
    delegate_id: str
    subject: str
    start_date: datetime.date
    end_date: datetime.date


@dataclass(slots=True, kw_only=True)
class CandidateDocument:
    id: str | None = field(default=None)
    candidate_id: str
    name: str
    url: str
