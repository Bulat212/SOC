from dataclasses import asdict

from app.domain.exception.answer import AnswerNotFound
from app.domain.model import Answer


class AnswerService:
    def add_answer(
            self,
            **data: str,
    ) -> Answer:
        answer = Answer(**data)
        return answer

    def get_answer(self, answer: Answer | None) -> dict[str, str]:
        if not answer:
            raise AnswerNotFound()
        data = asdict(answer)
        return data
