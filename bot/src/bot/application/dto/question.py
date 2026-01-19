from dataclasses import dataclass


@dataclass(slots=True)
class AddQuestionDTO:
    telegram_id: str
    question: str


@dataclass(slots=True)
class GetQuestionDTO:
    id: str
    number: int | None
    question: str
    user_id: str
    is_answer: bool


@dataclass(slots=True)
class AddQuestionIDDTO:
    question_id: str


@dataclass(slots=True)
class GetQuestionListDTO:
    total: int
    limit: int
    offset: int
    values: list[GetQuestionDTO]
