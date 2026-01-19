from pydantic import Field

from app.presentation.schema.base import Base


class GetStatusSchema(Base):
    id: str = Field(...)
    candidate_id: str = Field(...)
    status: str = Field(...)
