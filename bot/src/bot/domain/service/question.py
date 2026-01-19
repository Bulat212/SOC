from dataclasses import asdict

from bot.domain.exception.question import QuestionNotFound
from bot.domain.model.question import Question


class QuestionService:
    def get_question(self, question: Question | None) -> dict[str, str | bool]:
        if not question:
            raise QuestionNotFound
        data = asdict(question)
        return data
