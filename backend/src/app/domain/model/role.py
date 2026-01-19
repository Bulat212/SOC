from dataclasses import dataclass, field
from enum import StrEnum


class RoleEnum(StrEnum):
    CANDIDATE = "CANDIDATE"
    DELEGATE = "DELEGATE"
    DIRECTOR = "DIRECTOR"


@dataclass(slots=True, kw_only=True)
class Role:
    id: str | None = field(default=None)
    name: RoleEnum
