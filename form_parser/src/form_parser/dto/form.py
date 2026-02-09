from dataclasses import dataclass
import datetime

@dataclass
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
    date_issue_diploma: str | None
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
