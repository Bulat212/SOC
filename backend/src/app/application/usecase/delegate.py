from dataclasses import asdict

from app.application.interface.gateway.delegate import IDelegateDBGateway
from app.application.interface.db import DBSession
from app.application.dto.delegate import AddDelegateDTO, GetDelegateDTO, GetDelegateIDDTO, UpdateDelegateDTO
from app.domain.service.delegate import DelegateService
from app.application.interface.gateway.role import IRoleDBGateway
from app.application.interface.ulid_generator import ULIDGenerator


class DelegateUseCase:
    def __init__(
            self,
            delegate_gateway: IDelegateDBGateway,
            db_session: DBSession,
            delegate_service: DelegateService,
            role_db_gateway: IRoleDBGateway,
            ulid_generator: ULIDGenerator,
    ) -> None:
        self.delegate_gateway = delegate_gateway
        self.db_session = db_session
        self.delegate_service = delegate_service
        self.role_db_gateway = role_db_gateway
        self.ulid_generator = ulid_generator

    async def get(self, request: GetDelegateIDDTO) -> GetDelegateDTO:

        delegate = await self.delegate_gateway.get(
            telegram_id=request.telegram_id,
        )
        delegate = self.delegate_service.get_delegate_as_dict(delegate)
        return GetDelegateDTO(
            id=delegate.get("id"),
            telegram_id=delegate.get("telegram_id"),
            user_id=delegate.get("user_id"),
            first_name=delegate.get("first_name"),
            last_name=delegate.get("last_name"),
            patronymic=delegate.get("patronymic"),
            post=delegate.get("post"),
            subject=delegate.get("subject"),
            start_date=delegate.get("start_date"),
            end_date=delegate.get("end_date"),
        )
    
    async def update(self, request: UpdateDelegateDTO) -> GetDelegateDTO:
        delegate = await self.delegate_gateway.get(
            telegram_id=request.telegram_id,
        )
        delegate = self.delegate_service.get_delegate(delegate)
        delegate = self.delegate_service.update_delegate(
            delegate=delegate,
            **asdict(request),
        )
        await self.delegate_gateway.update(delegate=delegate)
        data = self.delegate_service.get_delegate_as_dict(delegate)

        await self.db_session.commit()
        return GetDelegateDTO(**data)
    

    async def add(self, request: AddDelegateDTO) -> GetDelegateDTO:
        delegate = self.delegate_service.add_delegate(
            **asdict(request),
            id=str(self.ulid_generator()),
        )
        delegate = await self.delegate_gateway.insert(delegate)
        data = self.delegate_service.get_delegate_as_dict(delegate=delegate)
        await self.db_session.commit()
        return GetDelegateDTO(**data)