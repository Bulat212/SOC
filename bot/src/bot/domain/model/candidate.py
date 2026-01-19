import datetime
from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True)
class Candidate:
    id: str | None = field(default=None)
    username: str | None = field(default=None)
    telegram_id: str
    recruitment_id: str
    nationality: str
    first_name: str
    last_name: str
    patronymic: str
    birthdate: datetime.date
    graduation_date: datetime.date
    subject: str
    military_station: str
    military_station_address: str
    university: str
    direction_training: str
    average_score: float
    find_out: str
    phone_number: str
    is_form: bool | None = field(default=False)
    is_statement: bool | None = field(default=False)
    is_approval: bool | None = field(default=False)
