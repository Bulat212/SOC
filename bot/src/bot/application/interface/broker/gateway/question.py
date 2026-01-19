from abc import abstractmethod
from typing import Protocol

from bot.domain.model.question import Question, QuestionList


class IQuestionBrokerGateway(Protocol):
    @abstractmethod
    async def add_question(self,
            telegram_id: str,
            question: str,
    ) -> Question | None: ...

    @abstractmethod
    async def get_question(self, question_id: str) -> Question | None: ...

    @abstractmethod
    async def get_question_list(
            self,
            limit: int,
            offset: int,
    ) -> QuestionList: ...
