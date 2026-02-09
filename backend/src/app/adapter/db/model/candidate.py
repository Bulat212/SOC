import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.adapter.db.model import BaseModel
from app.adapter.db.model.abstract_document import IDocument


class CandidateStorage(BaseModel):
    __tablename__ = "candidates"

    telegram_id: Mapped[str] = mapped_column(
        nullable=True,
        index=True,
        unique=True,
    )
    recruitment_id: Mapped[str]
    nationality: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    patronymic: Mapped[str]
    birthdate: Mapped[datetime.date]
    subject: Mapped[str]
    military_station: Mapped[str]
    military_station_address: Mapped[str]
    university: Mapped[str]
    graduation_date: Mapped[datetime.date]
    direction_training: Mapped[str]
    average_score: Mapped[float] = mapped_column(
        index=True,
    )
    find_out: Mapped[str]
    phone_number: Mapped[str] = mapped_column(
        index=True,
    )
    is_form: Mapped[bool] = mapped_column(
        default=False,
        server_default="true",
    )
    is_statement: Mapped[bool] = mapped_column(
        default=False,
        server_default="false",
    )
    is_approval: Mapped[bool] = mapped_column(
        default=False,
        server_default="false",
    )


class CandidateQuoteStorage(BaseModel):
    __tablename__ = "candidate_quotes"

    total: Mapped[int]
    count: Mapped[int]
    approved: Mapped[int]
    delegate_id: Mapped[str] = mapped_column(
        index=True,
    )
    subject: Mapped[str] = mapped_column(
        index=True,
    )
    start_date: Mapped[datetime.date]
    end_date: Mapped[datetime.date]


class CandidateStatementStorage(IDocument):
    __tablename__ = "candidate_statements"

    candidate_id: Mapped[str] = mapped_column(
        ForeignKey("candidates.id"),
        index=True,
    )


class CandidateApprovalStorage(IDocument):
    __tablename__ = "candidate_approvals"

    candidate_id: Mapped[str] = mapped_column(
        ForeignKey("candidates.id"),
        index=True,
    )


class CandidateFormStorage(IDocument):
    __tablename__ = "candidate_forms"

    candidate_id: Mapped[str] = mapped_column(
        ForeignKey("candidates.id"),
        index=True,
    )


class CandidateFormDataStorage(BaseModel):
    __tablename__ = "candidate_form_data"
    telegram_id: Mapped[str]
    candidate_id: Mapped[str]
    first_name: Mapped[str]= mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    patronymic: Mapped[str]= mapped_column(nullable=True)
    birthplace: Mapped[str]= mapped_column(nullable=True)
    birthdate: Mapped[datetime.date] = mapped_column(nullable=True)
    graduation_date: Mapped[datetime.date] = mapped_column(nullable=True)
    nationality: Mapped[str] = mapped_column(nullable=True)
    tg_username: Mapped[str] = mapped_column(nullable=True)
    mail: Mapped[str] = mapped_column(nullable=True)
    registration_address: Mapped[str] = mapped_column(nullable=True)
    actual_address: Mapped[str] = mapped_column(nullable=True)
    family_status: Mapped[str] = mapped_column(nullable=True)
    military_station: Mapped[str] = mapped_column(nullable=True)
    health_category: Mapped[str] = mapped_column(nullable=True)
    university: Mapped[str] = mapped_column(nullable=True)
    diploma: Mapped[str] = mapped_column(nullable=True)
    date_issue_diploma: Mapped[datetime.date] = mapped_column(nullable=True)
    direction_training: Mapped[str] = mapped_column(nullable=True)
    average_score: Mapped[float] = mapped_column(nullable=True)
    diploma_topic: Mapped[str] = mapped_column(nullable=True)
    international_articles: Mapped[str] = mapped_column(nullable=True)
    patents: Mapped[str] = mapped_column(nullable=True)
    vac_articles: Mapped[str] = mapped_column(nullable=True)
    rationalization: Mapped[str] = mapped_column(nullable=True)
    rinc_articles: Mapped[str] = mapped_column(nullable=True)
    registration_certificates: Mapped[str] = mapped_column(nullable=True)
    scientific_work_experience: Mapped[str] = mapped_column(nullable=True)
    international_olympiads: Mapped[str] = mapped_column(nullable=True)
    president_scholarship: Mapped[str] = mapped_column(nullable=True)
    russian_olympiads: Mapped[str] = mapped_column(nullable=True)
    government_scholarship: Mapped[str] = mapped_column(nullable=True)
    grant: Mapped[str] = mapped_column(nullable=True)
    regional_olympiads: Mapped[str] = mapped_column(nullable=True)
    city_olympiads: Mapped[str] = mapped_column(nullable=True)
    postgraduate_diploma: Mapped[str] = mapped_column(nullable=True)
    unused_academic_degree: Mapped[str] = mapped_column(nullable=True)
    useful_academic_degree: Mapped[str] = mapped_column(nullable=True)
    commercial_experience: Mapped[str] = mapped_column(nullable=True)
    OPK_experience: Mapped[str] = mapped_column(nullable=True)
    exp_research_assistant: Mapped[str] = mapped_column(nullable=True)
    areas_research: Mapped[str] = mapped_column(nullable=True)
    programming_languages: Mapped[str] = mapped_column(nullable=True)
    programs: Mapped[str] = mapped_column(nullable=True)
    secret: Mapped[str] = mapped_column(nullable=True)
    height: Mapped[str] = mapped_column(nullable=True)
    weight: Mapped[str] = mapped_column(nullable=True)
    sporting_achievements: Mapped[str] = mapped_column(nullable=True)
    other_sporting_achievements: Mapped[str] = mapped_column(nullable=True)
    short_run: Mapped[str] = mapped_column(nullable=True)
    long_run: Mapped[str] = mapped_column(nullable=True)
    pull_ups: Mapped[str] = mapped_column(nullable=True)
    chronic_diseases: Mapped[str] = mapped_column(nullable=True)
    tattoos: Mapped[str] = mapped_column(nullable=True)
    find_out: Mapped[str] = mapped_column(nullable=True)
