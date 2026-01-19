from abc import abstractmethod
from typing import Protocol

from app.domain.model import Answer


class IAnswerDBGateway(Protocol):
    @abstractmethod
    async def insert(self, answer: Answer) -> Answer: ...

    @abstractmethod
    async def get(self, answer_id: str) -> Answer | None: ...
