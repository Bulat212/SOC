from dataclasses import asdict

from bot.application.dto.candidate import (
    AddCandidateDTO,
    GetCandidateDTO,
    CandidateIDDTO,
    UpdateCandidateDTO,
    CandidateDocumentNameDTO,
)
from bot.application.dto.document import GetDocumentDTO, AddDocumentDTO
from bot.application.interface.broker.gateway.candidate import (
    ICandidateBrokerGateway
)
from bot.application.interface.broker.gateway.recruitment import (
    IRecruitmentBrokerGateway,
)
from bot.domain.model.candidate import Candidate
from bot.domain.service.candidate import CandidateService
from bot.domain.service.document import DocumentService
from bot.presentation.schema.candidate import GetCandidateSchema


class CandidateUseCase:
    def __init__(
            self,
            candidate_broker_gateway: ICandidateBrokerGateway,
            recruitment_broker_gateway: IRecruitmentBrokerGateway,
            candidate_service: CandidateService,
            document_service: DocumentService,
    ) -> None:
        self.candidate_broker_gateway = candidate_broker_gateway
        self.recruitment_broker_gateway = recruitment_broker_gateway
        self.candidate_service = candidate_service
        self.document_service = document_service

    async def add_candidate(self, request: AddCandidateDTO) -> GetCandidateSchema:
        candidate = self.candidate_service.add_candidate(**asdict(request))
        candidate = await self.candidate_broker_gateway.add_candidate(candidate)
        return candidate

    async def get_candidate(
            self,
            request: CandidateIDDTO,
    ) -> GetCandidateDTO:
        candidate = await self.candidate_broker_gateway.get_candidate(
            telegram_id=request.telegram_id,
        )
        recruitment = await self.recruitment_broker_gateway.get_recruitment(
            recruitment_id=candidate.recruitment_id,
        )
        data = self.candidate_service.get_candidate(
            recruitment=recruitment,
            candidate=candidate,
        )
        return GetCandidateDTO(**data)

    async def get_candidates_by_recruitment(self, recruitment_id, limit: int, offset: int):
        candidate_list = await self.candidate_broker_gateway.load_candidates(
            recruitment_id = recruitment_id,
            limit = limit,
            offset = offset,
        )
        return candidate_list

    async def update_candidate(
            self,
            request: UpdateCandidateDTO,
    ) -> GetCandidateSchema:
        candidate = await self.candidate_broker_gateway.get_candidate(
            telegram_id=request.telegram_id,
        )
        candidate = self.candidate_service.update_candidate(
            candidate,
            **asdict(request),
        )
        update_candidate = await self.candidate_broker_gateway.update_candidate(candidate)
        return update_candidate
    
    async def get_candidate_document(
            self,
            request: CandidateDocumentNameDTO,
    ) -> GetDocumentDTO:
        document = await self.candidate_broker_gateway.get_candidate_document(
            telegram_id=request.telegram_id,
            name=request.name,
        )
        data = self.document_service.get_document(document)
        return GetDocumentDTO(**data)

    async def add_or_update_form(
            self,
            request: AddDocumentDTO,
    ) -> None:
        await self._add_or_update_document(
            request=request,
            method="add_or_update_form",
        )

    async def add_or_update_approval(
            self,
            request: AddDocumentDTO,
    ) -> None:
        await self._add_or_update_document(
            request=request,
            method="add_or_update_approval",
        )

    async def add_or_update_statement(
            self,
            request: AddDocumentDTO,
    ) -> None:
        await self._add_or_update_document(
            request=request,
            method="add_or_update_statement",
        )

    async def _add_or_update_document(
            self,
            request: AddDocumentDTO,
            method: str,
    ) -> None:
        file = self.document_service.to_file_base64(request.file)
        document_buff = self.document_service.get_document_buff(
            name=request.name,
            file=file,
            filename=request.filename,
            candidate_id=request.candidate_id,
        )
        cls_method = getattr(self.candidate_broker_gateway, method)
        await cls_method(document_buff)

        
    async def delete(self, candidate_id: str, telegram_id: str):
        await self.candidate_broker_gateway.delete(candidate_id, telegram_id)

    async def new_registration_soc(self, form_data: Candidate):
        await self.candidate_broker_gateway.new_registration_soc(form_data=form_data)