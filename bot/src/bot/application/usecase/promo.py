from bot.application.dto.document import (
    AddDocumentNameDTO,
    GetDocumentsNameDTO,
    GetDocumentNameDTO,
    AddDocumentDTO,
    GetPromoDocumentDTO,
)
from bot.application.interface.broker.gateway.promo import IPromoBrokerGateway
from bot.domain.service.promo import PromoService


class PromoUseCase:
    def __init__(
            self,
            promo_broker_gateway: IPromoBrokerGateway,
            promo_service: PromoService,
    ) -> None:
        self.promo_broker_gateway = promo_broker_gateway
        self.promo_service = promo_service

    async def delete(self, request: AddDocumentNameDTO) -> None:
        await self.promo_broker_gateway.delete_promo_document(request.name)

    async def get(self, request: AddDocumentNameDTO) -> GetPromoDocumentDTO:
        document = await self.promo_broker_gateway.get_promo_document(
            name=request.name,
        )
        data = self.promo_service.get_promo(document)
        return GetPromoDocumentDTO(**data)

    async def get_name_all(self) -> GetDocumentsNameDTO:
        name_list = await self.promo_broker_gateway.get_promo_documents_name()
        result = []
        for val in name_list:
            result.append(GetDocumentNameDTO(name=val))
        return GetDocumentsNameDTO(
            values=result,
        )

    async def add(self, request: AddDocumentDTO) -> None:
        file = self.promo_service.to_file_base64(request.file)
        await self.promo_broker_gateway.add_promo_document(
            name=request.name,
            file=file,
            filename=request.filename,
        )
