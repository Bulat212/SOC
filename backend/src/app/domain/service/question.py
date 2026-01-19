from dataclasses import asdict

from app.domain.exception.question import QuestionNotFound
from app.domain.model import Question


class QuestionService:
    def get_number(self, number: int | None) -> int:
        if number is None:
            return 0
        return number + 1

    def add_question(self, **data: str | bool | int) -> Question:
        question = Question(
            id=data.get('id'),
            user_id=data.get('user_id'),
            question=data.get('question'),
            number=data.get('number'),
        )
        return question

    def get_question(
            self,
            question: Question | None,
    ) -> dict[str, str | int | bool]:
        if not question:
            raise QuestionNotFound()
        data = asdict(question)
        return data
