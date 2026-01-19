from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True)
class Question:
    id: str | None = field(default=None)
    user_id: str
    number: int | None = field(default=None)
    question: str
    is_answer: bool = field(default=False)


@dataclass(slots=True, kw_only=True)
class QuestionList:
    limit: int
    offset: int
    total: int
    values: list[Question]
