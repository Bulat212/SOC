from abc import abstractmethod
from collections.abc import AsyncIterator
from typing import Protocol

from app.domain.model import Delegate


class IDelegateDBGateway(Protocol):
    @abstractmethod
    async def insert(self, delegate: Delegate) -> Delegate: ...

    @abstractmethod
    async def update(self, delegate: Delegate) -> Delegate: ...

    @abstractmethod
    async def get(self, telegram_id: str) -> Delegate | None: ...

    @abstractmethod
    async def all(
            self,
            limit: int,
            offset: int,
    ) -> AsyncIterator[Delegate]: ...
