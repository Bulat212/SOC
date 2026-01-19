from abc import abstractmethod
from typing import Protocol

from app.domain.model import Info


class IInfoDBGateway(Protocol):
    @abstractmethod
    async def get(self) -> Info | None: ...
