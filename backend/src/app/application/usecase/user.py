from app.application.dto.user import GetUserIDDTO, GetUserDTO, GetUsersIDDTO
from app.application.interface.db import DBSession
from app.application.interface.gateway.role import IRoleDBGateway
from app.application.interface.gateway.user import IUserDBGateway
from app.application.interface.ulid_generator import ULIDGenerator
from app.domain.model.role import RoleEnum
from app.domain.service.role import RoleService
from app.domain.service.user import UserService


class UserUseCase:
    def __init__(
            self,
            user_gateway: IUserDBGateway,
            role_gateway: IRoleDBGateway,
            ulid_generator: ULIDGenerator,
            db_session: DBSession,
            user_service: UserService,
            role_service: RoleService,
    ) -> None:
        self.user_gateway = user_gateway
        self.ulid_generator = ulid_generator
        self.db_session = db_session
        self.role_gateway = role_gateway
        self.user_service = user_service
        self.role_service = role_service

    async def get(self, request: GetUserIDDTO) -> GetUserDTO:
        user = await self.user_gateway.get(
            telegram_id=request.telegram_id,
            user_id=request.id,
        )
        user = self.user_service.get_user(user)
        role = await self.role_gateway.get(role_id=user.get("role_id"))
        role = self.role_service.get_role(role)
        return GetUserDTO(
            id=user.get("id"),
            telegram_id=user.get("telegram_id"),
            username=user.get("username"),
            first_name=user.get("first_name"),
            last_name=user.get("last_name"),
            role=role.get("name"),
            is_active=user.get("is_active"),
        )

    async def get_director_id_all(self) -> GetUsersIDDTO:
        role = await self.role_gateway.get_role(
            name=RoleEnum.DIRECTOR,
        )
        role_id = self.role_service.get_role_id(role)
        user_id_list = await self.user_gateway.get_id_all(role_id=role_id)
        return GetUsersIDDTO(
            values=[
                GetUserIDDTO(
                    telegram_id=val,
                )
                for val in user_id_list
            ],
        )
    
    async def delete_user(self, user_id: str):
        await self.user_gateway.delete(user_id)
        await self.db_session.commit()
