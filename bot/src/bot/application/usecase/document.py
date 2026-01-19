from bot.application.dto.candidate import CandidateDocumentNameDTO
from bot.application.dto.document import AddDocumentNameDTO, GetDocumentDTO
from bot.application.interface.broker.gateway.document import (
    IDocumentBrokerGateway,
)
from bot.domain.service.document import DocumentService


class DocumentUseCase:
    def __init__(
            self,
            document_broker_gateway: IDocumentBrokerGateway,
            document_service: DocumentService,
    ) -> None:
        self.document_broker_gateway = document_broker_gateway
        self.document_service = document_service

    async def get(self, request: AddDocumentNameDTO) -> GetDocumentDTO:
        document = await self.document_broker_gateway.get_document(
            name=request.name,
        )
        data = self.document_service.get_document(document)
        return GetDocumentDTO(**data)
