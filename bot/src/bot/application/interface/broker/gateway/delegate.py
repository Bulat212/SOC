from abc import abstractmethod
from typing import Protocol

from bot.domain.model import Delegate


class IDelegateBrokerGateway(Protocol):
    @abstractmethod
    async def get_delegate(self, telegram_id: str) -> Delegate | None: ...

    @abstractmethod
    async def update_delegate(self, delegate: Delegate) -> None: ...

    @abstractmethod
    async def add_delegate(self, delegate: Delegate) -> None: ...

