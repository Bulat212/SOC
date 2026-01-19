from dataclasses import dataclass, field
from enum import StrEnum

class StatusEnum(StrEnum):
    REVIEWED = "REVIEWED"
    REJECTED = "REJECTED"
    UNDER_REVIEW = "UNDER_REVIEW"


@dataclass(slots=True, kw_only=True)
class Status:
    id: str | None = field(default=None)
    candidate_id: str
    status: StatusEnum
