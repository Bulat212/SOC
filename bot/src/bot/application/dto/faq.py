from dataclasses import dataclass


@dataclass(slots=True, kw_only=True)
class AddFaqIDDTO:
    id: str


@dataclass(slots=True, kw_only=True)
class GetFaqDTO:
    id: str
    question: str
    answer: str


@dataclass(slots=True, kw_only=True)
class GetFaqListDTO:
    total: int
    limit: int
    offset: int
    values: list[GetFaqDTO]


@dataclass(slots=True, kw_only=True)
class AddFaqDTO:
    question: str
    answer: str
