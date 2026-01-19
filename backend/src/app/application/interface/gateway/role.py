from abc import abstractmethod
from typing import Protocol

from app.domain.model import Role


class IRoleDBGateway(Protocol):
    @abstractmethod
    async def get(self, role_id: str) -> Role | None: ...

    @abstractmethod
    async def get_role(self, name: str) -> Role | None: ...
