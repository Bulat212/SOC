from abc import abstractmethod
from typing import Protocol

from app.domain.model import Recruitment


class IRecruitmentDBGateway(Protocol):
    @abstractmethod
    async def insert(self, recruitment: Recruitment) -> Recruitment: ...

    @abstractmethod
    async def get(self, recruitment_id: str) -> Recruitment | None: ...

    @abstractmethod
    async def delete(self, name: str) -> None: ...

    @abstractmethod
    async def update(self, name: str) -> Recruitment: ...

    @abstractmethod
    async def all(self) -> list[Recruitment]: ...
