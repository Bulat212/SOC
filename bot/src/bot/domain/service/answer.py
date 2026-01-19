from bot.domain.model.answer import Answer


class AnswerService:
    def add_answer(self, **data: str) -> Answer:
        answer = Answer(**data)
        return answer
