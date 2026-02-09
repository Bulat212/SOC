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


@dataclass(slots=True, kw_only=True)
class CandidateFormData:
    id: str | None = field(default=None)
    telegram_id: str | None = field(default=None)
    candidate_id: str | None = field(default=None)
    first_name: str
    last_name: str
    patronymic: str
    birthplace: str
    birthdate: datetime.date
    graduation_date: datetime.date
    nationality: str
    tg_username: str | None = field(default=None)
    mail: str
    registration_address: str
    actual_address: str
    family_status: str
    military_station: str
    health_category: str
    university: str
    diploma: str
    date_issue_diploma: datetime.date
    direction_training: str
    average_score: float
    diploma_topic: str
    international_articles: str
    patents: str
    vac_articles: str
    rationalization: str
    rinc_articles: str
    registration_certificates: str
    scientific_work_experience: str
    international_olympiads: str
    president_scholarship: str
    russian_olympiads: str
    government_scholarship: str
    grant: str
    regional_olympiads: str
    city_olympiads: str
    postgraduate_diploma: str
    unused_academic_degree: str
    useful_academic_degree: str
    commercial_experience: str
    OPK_experience: str
    exp_research_assistant: str
    areas_research: str
    programming_languages: str
    programs: str
    secret: str
    height: str
    weight: str
    sporting_achievements: str
    other_sporting_achievements: str
    short_run: str
    long_run: str
    pull_ups: str
    chronic_diseases: str
    tattoos: str
    find_out: str
