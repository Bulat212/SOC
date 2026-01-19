from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True)
class AddQuestionDTO:
    user_id: str | None = field(default=None)
    telegram_id: str | None = field(default=None)
    question: str


@dataclass(slots=True, kw_only=True)
class GetQuestionDTO:
    id: str
    user_id: str | None = field(default=None)
    number: int | None
    question: str
    is_answer: bool


@dataclass(slots=True, kw_only=True)
class AddQuestionIDDTO:
    question_id: str


@dataclass(slots=True, kw_only=True)
class GetQuestionListDTO:
    limit: int
    offset: int
    total: int
    values: list[GetQuestionDTO]
