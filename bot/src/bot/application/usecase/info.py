from bot.application.dto.info import GetInfoDTO
from bot.application.interface.broker.gateway.info import IInfoBrokerGateway
from bot.domain.service.info import InfoService


class InfoUseCase:
    def __init__(
            self,
            info_broker_gateway: IInfoBrokerGateway,
            info_service: InfoService,
    ) -> None:
        self.info_broker_gateway = info_broker_gateway
        self.info_service = info_service

    async def get_info(self) -> GetInfoDTO:
        info = await self.info_broker_gateway.get_info()
        data = self.info_service.get_info(info)
        return GetInfoDTO(**data)
