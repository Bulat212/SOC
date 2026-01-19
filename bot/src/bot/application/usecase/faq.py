from dataclasses import asdict

from bot.application.dto.faq import (
    AddFaqIDDTO,
    GetFaqDTO,
    GetFaqListDTO,
    AddFaqDTO,
)
from bot.application.dto.pagination import PaginationDTO
from bot.application.interface.broker.gateway.faq import IFaqBrokerGateway
from bot.constants import ZERO
from bot.domain.exception.faq import FaqNotFound
from bot.domain.service.faq import FaqService


class FaqUseCase:
    def __init__(
            self,
            faq_broker_gateway: IFaqBrokerGateway,
            faq_service: FaqService,
    ) -> None:
        self.faq_broker_gateway = faq_broker_gateway
        self.faq_service = faq_service

    async def delete(self, request: AddFaqIDDTO) -> None:
        await self.faq_broker_gateway.delete_faq(request.id)

    async def add(self, request: AddFaqDTO) -> None:
        faq = self.faq_service.add_faq(**asdict(request))
        await self.faq_broker_gateway.add_faq(faq)

    async def get(self, request: AddFaqIDDTO) -> GetFaqDTO:
        faq = await self.faq_broker_gateway.get_faq(faq_id=request.id)
        data = self.faq_service.get_faq(faq)
        return GetFaqDTO(**data)

    async def get_all(self, request: PaginationDTO) -> GetFaqListDTO:
        faq_list = await self.faq_broker_gateway.get_faq_list(
            limit=request.limit,
            offset=request.offset,
        )
        try:
            data = self.faq_service.get_faq_list(faq_list)
        except FaqNotFound:
            return GetFaqListDTO(
                limit=request.limit,
                offset=request.offset,
                total=ZERO,
                values=[],
            )
        values: dict[str, str] | None = data.get("values")
        result = []
        for val in values:
            result.append(GetFaqDTO(**val))
        return GetFaqListDTO(
            limit=request.limit,
            offset=request.offset,
            total=data.get("total"),
            values=result,
        )
