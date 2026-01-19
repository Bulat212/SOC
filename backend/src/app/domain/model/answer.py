from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True)
class Answer:
    id: str | None = field(default=None)
    question_id: str
    answer: str
