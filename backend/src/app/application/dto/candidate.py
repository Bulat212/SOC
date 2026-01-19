import datetime
from dataclasses import dataclass

from app.application.dto.pagination import PaginationDTO


@dataclass(slots=True, kw_only=True)
class AddCandidateDTO:
    telegram_id: str | None
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
    university: str
    graduation_date: datetime.date
    direction_training: str
    average_score: float
    find_out: str
    phone_number: str


@dataclass(slots=True, kw_only=True)
class GetCandidateDTO:
    id: str
    telegram_id: str | None
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
    is_form: bool
    is_statement: bool
    is_approval: bool


@dataclass(slots=True, kw_only=True)
class UpdateCandidateDTO:
    id: str | None
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
class AddCandidateIDDTO:
    id: str | None
    telegram_id: str | None


@dataclass(slots=True, kw_only=True)
class CandidateDocumentNameDTO:
    id: str | None
    telegram_id: str | None
    name: str


@dataclass(slots=True, kw_only=True)
class GetCandidatesDTO:
    limit: int
    offset: int
    total: int
    values: list[GetCandidateDTO]


@dataclass(slots=True, kw_only=True)
class AddCandidateQuoteDTO:
    total: int
    count: int
    approved: int
    delegate_id: str
    subject: str
    date: datetime.date


@dataclass(slots=True, kw_only=True)
class GetCandidateQuoteDTO:
    id: str
    count: int
    approved: int
    delegate_id: str
    subject: str
    date: datetime.date


@dataclass(slots=True, kw_only=True)
class UpdateCandidateQuoteDTO:
    count: int | None
    approved: int | None
    delegate_id: str
    subject: str | None
    date: datetime.date | None


@dataclass(slots=True, kw_only=True)
class CandidateQuotePaginationDTO(PaginationDTO):
    delegate_id: str
