from abc import abstractmethod
from typing import Protocol

from app.domain.model import Document
from app.domain.model.document import PromoDocument


class IDocumentDBGateway(Protocol):
    @abstractmethod
    async def get(self, info_id: str, name: str) -> Document | None: ...


class IPromoDocumentDBGateway(IDocumentDBGateway, Protocol):
    @abstractmethod
    async def get(self, info_id: str, name: str) -> PromoDocument | None: ...

    @abstractmethod
    async def get_name_all(self) -> list[str]: ...

    @abstractmethod
    async def insert(self, document: PromoDocument) -> PromoDocument: ...

    @abstractmethod
    async def delete(self, name: str) -> None: ...
