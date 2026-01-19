from pydantic import Field

from app.presentation.schema.base import Base


class GetRecruitmentSchema(Base):
    id: str = Field(...)
    name: str = Field(...)


class GetRecruitmentsSchema(Base):
    values: list[GetRecruitmentSchema]


class AddRecruitmentIDSchema(Base):
    id: str = Field(...)
