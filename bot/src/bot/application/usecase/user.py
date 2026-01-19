from bot.application.dto.user import (
    UserIDDTO,
    GetUserDTO,
    GetUsersIDDTO,
    GetUserIDDTO,
)
from bot.application.interface.broker.gateway.user import IUserBrokerGateway
from bot.domain.service.user import UserService


class UserUseCase:
    def __init__(
            self,
            user_broker_gateway: IUserBrokerGateway,
            user_service: UserService,
    ) -> None:
        self.user_broker_gateway = user_broker_gateway
        self.user_service = user_service

    async def get(self, request: UserIDDTO) -> GetUserDTO:
        user = await self.user_broker_gateway.get_user(request.telegram_id)
        user = self.user_service.get_user(user)
        return GetUserDTO(**user)

    async def get_director_id_all(self) -> GetUsersIDDTO:
        user_id_list = await self.user_broker_gateway.get_users_director_id()
        result = []
        for val in user_id_list:
            result.append(
                GetUserIDDTO(
                    telegram_id=val,
                ),
            )
        return GetUsersIDDTO(
            values=result,
        )
    
    async def delete(self, user_id: str):
        await self.user_broker_gateway.delete(user_id)

