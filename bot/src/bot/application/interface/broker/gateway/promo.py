from abc import abstractmethod
from typing import Protocol

from bot.domain.model.document import PromoDocument


class IPromoBrokerGateway(Protocol):
    @abstractmethod
    async def get_promo_document(self, name: str) -> PromoDocument | None: ...

    @abstractmethod
    async def get_promo_documents_name(self) -> list[str]: ...

    @abstractmethod
    async def add_promo_document(self,
            name: str,
            file: str,
            filename: str,
    ) -> None: ...

    @abstractmethod
    async def delete_promo_document(self, name: str) -> None: ...
