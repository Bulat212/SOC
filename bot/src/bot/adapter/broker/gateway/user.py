import json

from faststream.rabbit.message import RabbitMessage

from bot.adapter.broker.gateway.base import BaseBrokerGateway
from bot.constants import TIMEOUT
from bot.domain.model import User


class UserBrokerGateway(BaseBrokerGateway):
    async def get_user(self, user_id: str) -> User | None:
        try:
            msg: RabbitMessage = await self.broker.request(
                message={
                    "telegram_id": user_id,
                },
                queue="get_user",
                timeout=TIMEOUT,
            )
        except TimeoutError:
            return None
        body = json.loads(msg.body)
        return User(**body)

    async def get_users_director_id(self) -> list[str]:
        try:
            msg: RabbitMessage = await self.broker.request(
                message={},
                queue="get_users_director_id",
                timeout=TIMEOUT,
            )
        except TimeoutError:
            return []
        body = json.loads(msg.body)
        result = []
        for val in body.get("values", []):
            result.append(val.get("telegram_id"))
        return result


    async def delete(self, user_id: str): 
        await self.broker.publish(
            message={
                "user_id": user_id,
            },
            queue="delete_user"
        )