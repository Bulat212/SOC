import json

from faststream.rabbit.message import RabbitMessage

from bot.adapter.broker.gateway.base import BaseBrokerGateway
from bot.constants import TIMEOUT
from bot.domain.model.status import Status


class StatusBrokerGateway(BaseBrokerGateway):
    async def get_status(self, telegram_id: str) -> Status | None:
        try:
            msg: RabbitMessage = await self.broker.request(
                message={
                    "telegram_id": telegram_id,
                },
                queue="get_status",
                timeout=TIMEOUT,
            )
        except TimeoutError:
            return None
        body = json.loads(msg.body)
        return Status(**body)
