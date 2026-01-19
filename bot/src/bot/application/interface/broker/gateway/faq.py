from abc import abstractmethod
from typing import Protocol

from bot.domain.model.faq import Faq, FaqList


class IFaqBrokerGateway(Protocol):
    @abstractmethod
    async def get_faq(self, faq_id: str) -> Faq | None: ...

    @abstractmethod
    async def get_faq_list(self,
            limit: int,
            offset: int,
    ) -> FaqList | None: ...

    @abstractmethod
    async def add_faq(self, faq: Faq) -> None: ...

    @abstractmethod
    async def delete_faq(self, faq_id: str) -> None: ...
