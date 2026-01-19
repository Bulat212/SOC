from abc import abstractmethod
from typing import Protocol

from bot.domain.model.status import Status


class IStatusBrokerGateway(Protocol):
    @abstractmethod
    async def get_status(self, telegram_id: str) -> Status | None: ...
