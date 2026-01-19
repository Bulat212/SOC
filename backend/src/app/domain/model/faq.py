from dataclasses import dataclass, field


@dataclass(kw_only=True, slots=True)
class Faq:
    id: str | None = field(default=None)
    question: str
    answer: str
