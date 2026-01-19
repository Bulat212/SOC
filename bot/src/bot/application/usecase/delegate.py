from dataclasses import asdict

from bot.application.dto.delegate import AddDelegateDTO, DelegateIDDTO, GetDelegateDTO, UpdateDelegateDTO
from bot.application.interface.broker.gateway.delegate import IDelegateBrokerGateway
from bot.domain.service.delegate import DelegateService


class DelegateUseCase:
    def __init__(
            self,
            delegate_broker_gateway: IDelegateBrokerGateway,
            delegate_service: DelegateService,
    ) -> None:
        self.delegate_broker_gateway = delegate_broker_gateway
        self.delegate_service = delegate_service


    async def get(self, request: DelegateIDDTO) -> GetDelegateDTO:
        delegate = await self.delegate_broker_gateway.get_delegate(request.telegram_id)      
        delegate = self.delegate_service.get_delegate(delegate)
        return GetDelegateDTO(**delegate)
    

    async def add_delegate(self, request: AddDelegateDTO) -> None:
        delegate = self.delegate_service.add_delegate(**asdict(request))
        await self.delegate_broker_gateway.add_delegate(delegate)
    

    async def update_delegate(
            self,
            request: UpdateDelegateDTO,
    ) -> None:
        delegate = await self.delegate_broker_gateway.get_delegate(telegram_id=request.telegram_id)
        delegate = self.delegate_service.update_delegate(
            delegate,
            **asdict(request),
        )
        await self.delegate_broker_gateway.update_delegate(delegate)


