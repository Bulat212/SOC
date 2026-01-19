import datetime

from pydantic import Field

from .base import Base


class AddCandidateSchema(Base):
    username: str | None = Field(None)
    telegram_id: str = Field(...)
    recruitment_id: str = Field(...)
    nationality: str = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    patronymic: str = Field(...)
    birthdate: datetime.date = Field(...)
    military_station: str = Field(...)
    military_station_address: str = Field(...)
    university: str = Field(...)
    graduation_date: datetime.date = Field(...)
    direction_training: str = Field(...)
    average_score: float = Field(...)
    find_out: str = Field(...)
    phone_number: str = Field(...)
    subject: str = Field(...)


class GetCandidateSchema(Base):
    id: str = Field(...)
    telegram_id: str = Field(...)
    recruitment_id: str = Field(...)
    nationality: str = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    patronymic: str = Field(...)
    birthdate: datetime.date = Field(...)
    military_station: str = Field(...)
    military_station_address: str = Field(...)
    university: str = Field(...)
    direction_training: str = Field(...)
    graduation_date: datetime.date = Field(...)
    average_score: float = Field(...)
    find_out: str = Field(...)
    phone_number: str = Field(...)
    subject: str = Field(...)
    is_form: bool = Field(...)
    is_statement: bool = Field(...)
    is_approval: bool = Field(...)


class UpdateCandidateSchema(Base):
    id: str | None = Field(None)
    telegram_id: str | None = Field(None)
    recruitment_id: str | None = Field(None)
    nationality: str | None = Field(None)
    first_name: str | None = Field(None)
    last_name: str | None = Field(None)
    patronymic: str | None = Field(None)
    birthdate: datetime.date | None = Field(None)
    military_station: str | None = Field(None)
    military_station_address: str | None = Field(None)
    university: str | None = Field(None)
    graduation_date: datetime.date | None = Field(None)
    direction_training: str | None = Field(None)
    average_score: float | None = Field(None)
    find_out: str | None = Field(None)
    phone_number: str | None = Field(None)
    subject: str | None = Field(None)


class AddCandidateIDSchema(Base):
    id: str | None = Field(None)
    telegram_id: str | None = Field(None)


class CandidateDocumentNameSchema(Base):
    id: str | None = Field(None)
    telegram_id: str | None = Field(None)
    name: str = Field(...)

class DeleteCandidateSchema(Base):
    candidate_id: str | None = Field(None)
