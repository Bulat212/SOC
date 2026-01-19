from abc import abstractmethod
from typing import Protocol

from bot.domain.model.info import Info


class IInfoBrokerGateway(Protocol):
    @abstractmethod
    async def get_info(self) -> Info | None: ...
