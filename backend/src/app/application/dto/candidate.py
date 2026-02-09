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


@dataclass(slots=True, kw_only=True)
class FormDataDTO:
    telegram_id: str
    candidate_id: str
    first_name: str | None
    last_name: str | None
    patronymic: str | None
    birthplace: str | None
    birthdate: datetime.date | None
    graduation_date: datetime.date | None
    nationality: str | None
    tg_username: str | None
    mail: str | None
    registration_address: str | None
    actual_address: str | None
    family_status: str | None
    military_station: str | None
    health_category: str | None
    university: str | None
    diploma: str | None
    date_issue_diploma: datetime.date | None
    direction_training: str | None
    average_score: float | None
    diploma_topic: str | None
    international_articles: str | None
    patents: str | None
    vac_articles: str | None
    rationalization: str | None
    rinc_articles: str | None
    registration_certificates: str | None
    scientific_work_experience: str | None
    international_olympiads: str | None
    president_scholarship: str | None
    russian_olympiads: str | None
    government_scholarship: str | None
    grant: str | None
    regional_olympiads: str | None
    city_olympiads: str | None
    postgraduate_diploma: str | None
    unused_academic_degree: str | None
    useful_academic_degree: str | None
    commercial_experience: str | None
    OPK_experience: str | None
    exp_research_assistant: str | None
    areas_research: str | None
    programming_languages: str | None
    programs: str | None
    secret: str | None
    height: str | None
    weight: str | None
    sporting_achievements: str | None
    other_sporting_achievements: str | None
    short_run: str | None
    long_run: str | None
    pull_ups: str | None
    chronic_diseases: str | None
    tattoos: str | None
    find_out: str | None

