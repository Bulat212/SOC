from abc import abstractmethod
from collections.abc import AsyncIterator
from typing import Protocol

from app.domain.model import User


class IUserDBGateway(Protocol):
    @abstractmethod
    async def insert(self, user: User) -> User: ...

    @abstractmethod
    async def get(
            self,
            user_id: str | None = None,
            telegram_id: str | None = None,
    ) -> User | None: ...

    @abstractmethod
    async def all(self, limit: int, offset: int) -> AsyncIterator[User]: ...

    @abstractmethod
    async def update(self, user: User) -> User: ...

    @abstractmethod
    async def get_id_all(self, role_id: str) -> list[str]: ...

    @abstractmethod
    async def delete(self, user_id: str): ...