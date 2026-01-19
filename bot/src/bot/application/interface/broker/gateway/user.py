from abc import abstractmethod
from typing import Protocol

from bot.domain.model import User


class IUserBrokerGateway(Protocol):
    @abstractmethod
    async def get_user(self, user_id: str) -> User | None: ...

    @abstractmethod
    async def get_users_director_id(self) -> list[str]: ...
    
    @abstractmethod
    async def delete(self, user_id: str): ...
