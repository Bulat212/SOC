from pydantic import BaseModel, ConfigDict
import datetime

from pydantic import Field

class Base(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


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
