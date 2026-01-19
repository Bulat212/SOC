from dataclasses import asdict

from app.application.dto.faq import (
    AddFaqIDDTO,
    GetFaqDTO,
    GetFaqListDTO,
    AddFaqDTO,
)
from app.application.dto.pagination import PaginationDTO
from app.application.interface.db import DBSession
from app.application.interface.gateway.faq import IFaqDBGateway
from app.application.interface.ulid_generator import ULIDGenerator
from app.domain.service.faq import FaqService


class FaqUseCase:
    def __init__(
            self,
            faq_db_gateway: IFaqDBGateway,
            faq_service: FaqService,
            ulid_generator: ULIDGenerator,
            db_session: DBSession,
    ) -> None:
        self.faq_db_gateway = faq_db_gateway
        self.faq_service = faq_service
        self.ulid_generator = ulid_generator
        self.db_session = db_session

    async def delete(self, request: AddFaqIDDTO) -> None:
        await self.faq_db_gateway.delete(request.id)
        await self.db_session.commit()

    async def add(self, request: AddFaqDTO) -> GetFaqDTO:
        faq = self.faq_service.add_faq(
            faq_id=str(self.ulid_generator()),
            **asdict(request),
        )
        faq = await self.faq_db_gateway.insert(faq)
        data = self.faq_service.get(faq)
        await self.db_session.commit()
        return GetFaqDTO(**data)

    async def get(self, request: AddFaqIDDTO) -> GetFaqDTO:
        faq = await self.faq_db_gateway.get(request.id)
        data = self.faq_service.get(faq)
        return GetFaqDTO(**data)

    async def all(self, request: PaginationDTO) -> GetFaqListDTO:
        total = await self.faq_db_gateway.get_total()
        arr_faq = self.faq_db_gateway.all(
            limit=request.limit,
            offset=request.offset * request.limit,
        )
        result = []
        async for faq in arr_faq:
            data = self.faq_service.get(faq)
            result.append(GetFaqDTO(**data))
        return GetFaqListDTO(
            total=total,
            limit=request.limit,
            offset=request.offset,
            values=result,
        )
