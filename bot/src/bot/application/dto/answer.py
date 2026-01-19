from dataclasses import dataclass


@dataclass(slots=True)
class AddAnswerDTO:
    question_id: str
    answer: str
