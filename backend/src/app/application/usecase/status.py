from app.application.dto.candidate import AddCandidateIDDTO
from app.application.dto.status import GetStatusDTO
from app.application.interface.gateway.candidate import ICandidateDBGateway
from app.application.interface.gateway.status import IStatusDBGateway
from app.domain.service.candidate import CandidateService
from app.domain.service.status import StatusService


class StatusUseCase:
    def __init__(
            self,
            status_db_gateway: IStatusDBGateway,
            candidate_db_gateway: ICandidateDBGateway,
            candidate_service: CandidateService,
            status_service: StatusService,
    ) -> None:
        self.status_db_gateway = status_db_gateway
        self.candidate_db_gateway = candidate_db_gateway
        self.candidate_service = candidate_service
        self.status_service = status_service

    async def get(self, request: AddCandidateIDDTO) -> GetStatusDTO:
        candidate = await self.candidate_db_gateway.get(
            candidate_id=request.id,
            telegram_id=request.telegram_id,
        )
        candidate_id = self.candidate_service.get_candidate_id(candidate)
        status = await self.status_db_gateway.get(candidate_id)
        data = self.status_service.get_status(status)
        return GetStatusDTO(**data)
