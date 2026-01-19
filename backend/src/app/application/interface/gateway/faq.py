from abc import abstractmethod
from collections.abc import AsyncIterator
from typing import Protocol

from app.domain.model import Faq


class IFaqDBGateway(Protocol):
    @abstractmethod
    async def get(self, faq_id: str) -> Faq | None: ...

    @abstractmethod
    async def all(self, limit: int, offset: int) -> AsyncIterator[Faq]: ...

    @abstractmethod
    async def get_total(self) -> int: ...

    @abstractmethod
    async def insert(self, faq: Faq) -> Faq: ...

    @abstractmethod
    async def delete(self, faq_id: str) -> None: ...
