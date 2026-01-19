from abc import abstractmethod
from typing import Protocol

from bot.domain.model import Recruitment


class IRecruitmentBrokerGateway(Protocol):
    @abstractmethod
    async def get_recruitments(self) -> list[Recruitment]: ...

    @abstractmethod
    async def get_recruitment(self,
            recruitment_id: str,
    ) -> Recruitment | None: ...
