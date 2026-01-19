from abc import abstractmethod
from typing import Protocol

from bot.domain.model.document import Document


class IDocumentBrokerGateway(Protocol):
    @abstractmethod
    async def get_document(self, name: str) -> Document | None: ...
