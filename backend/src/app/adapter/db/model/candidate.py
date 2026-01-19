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
