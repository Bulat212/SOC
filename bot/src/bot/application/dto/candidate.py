import datetime
from dataclasses import dataclass


@dataclass(kw_only=True, slots=True)
class AddCandidateDTO:
    telegram_id: str
    recruitment_id: str
    nationality: str
    username: str | None
    first_name: str
    last_name: str
    patronymic: str
    birthdate: datetime.date
    subject: str
    military_station: str
    military_station_address: str
    direction_training: str
    university: str
    graduation_date: datetime.date
    average_score: float
    find_out: str
    phone_number: str


@dataclass(kw_only=True, slots=True)
class GetCandidateDTO:
    id: str
    telegram_id: str | None
    recruitment: str
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
    is_form: bool
    is_statement: bool
    is_approval: bool


@dataclass(kw_only=True, slots=True)
class CandidateIDDTO:
    telegram_id: str


@dataclass(kw_only=True, slots=True)
class UpdateCandidateDTO:
    telegram_id: str | None
    recruitment_id: str | None
    nationality: str | None
    first_name: str | None
    last_name: str | None
    patronymic: str | None
    birthdate: datetime.date | None
    subject: str | None
    military_station: str | None
    military_station_address: str | None
    university: str | None
    graduation_date: datetime.date | None
    direction_training: str | None
    average_score: float | None
    find_out: str | None
    phone_number: str | None


@dataclass(slots=True, kw_only=True)
class CandidateDocumentNameDTO:
    telegram_id: str
    name: str