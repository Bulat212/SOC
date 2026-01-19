from abc import abstractmethod
from typing import Protocol

from bot.domain.model.answer import Answer


class IAnswerBrokerGateway(Protocol):
    @abstractmethod
    async def add_answer(self, answer: Answer) -> None: ...
