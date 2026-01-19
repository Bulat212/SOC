from bot.application.dto.candidate import CandidateIDDTO
from bot.application.dto.status import GetStatusDTO
from bot.application.interface.broker.gateway.status import (
    IStatusBrokerGateway,
)
from bot.domain.service.status import StatusService


class StatusUseCase:
    def __init__(
            self,
            status_broker_gateway: IStatusBrokerGateway,
            status_service: StatusService,
    ) -> None:
        self.status_broker_gateway = status_broker_gateway
        self.status_service = status_service

    async def get(self, request: CandidateIDDTO) -> GetStatusDTO:
        status = await self.status_broker_gateway.get_status(
            telegram_id=request.telegram_id,
        )
        data = self.status_service.get_status(status)
        return GetStatusDTO(**data)
