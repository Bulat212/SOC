from dataclasses import dataclass


@dataclass(slots=True, kw_only=True)
class AddAnswerDTO:
    question_id: str
    answer: str


@dataclass(slots=True, kw_only=True)
class GetAnswerDTO:
    id: str
    question_id: str
    answer: str


@dataclass(slots=True, kw_only=True)
class AnswerIDDTO:
    id: str
