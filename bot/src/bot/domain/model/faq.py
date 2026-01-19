from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True)
class Faq:
    id: str | None = field(default=None)
    question: str
    answer: str


@dataclass(slots=True, kw_only=True)
class FaqList:
    total: int
    limit: int
    offset: int
    values: list[Faq]
