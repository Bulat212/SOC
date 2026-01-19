from abc import abstractmethod
from typing import Protocol

from app.domain.model import Status


class IStatusDBGateway(Protocol):
    @abstractmethod
    async def insert(self, status: Status) -> Status: ...

    @abstractmethod
    async def get(self, candidate_id: str) -> Status | None: ...

    @abstractmethod
    async def update_status(self, is_status: bool) -> Status: ...

    @abstractmethod
    async def delete(self, candidate_id: str): ...