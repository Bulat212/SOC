from app.application.dto.info import GetInfoDTO
from app.application.interface.gateway.info import IInfoDBGateway
from app.domain.service.info import InfoService


class InfoUseCase:
    def __init__(
            self,
            info_db_gateway: IInfoDBGateway,
            info_service: InfoService,
    ) -> None:
        self.info_db_gateway = info_db_gateway
        self.info_service = info_service

    async def get(self) -> GetInfoDTO:
        info = await self.info_db_gateway.get()
        data = self.info_service.get_info(info)
        return GetInfoDTO(**data)
