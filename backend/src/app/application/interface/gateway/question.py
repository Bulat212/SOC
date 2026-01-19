from abc import abstractmethod
from collections.abc import AsyncIterable
from typing import Protocol

from app.domain.model import Question


class IQuestionDBGateway(Protocol):
    @abstractmethod
    async def insert(self, question: Question) -> Question: ...

    @abstractmethod
    async def get(self, question_id: str) -> Question | None: ...

    @abstractmethod
    async def all(
            self,
            limit: int,
            offset: int,
    ) -> AsyncIterable[Question]: ...

    @abstractmethod
    async def change_status(self,
            question_id: str,
            is_answer: bool,
    ) -> None: ...

    @abstractmethod
    async def get_total(self) -> int: ...

    @abstractmethod
    async def get_number(self) -> int | None: ...
