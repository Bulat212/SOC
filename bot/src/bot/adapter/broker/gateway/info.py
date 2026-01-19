import json

from faststream.rabbit.message import RabbitMessage

from bot.adapter.broker.gateway.base import BaseBrokerGateway
from bot.constants import TIMEOUT
from bot.domain.model.info import Info


class InfoBrokerGateway(BaseBrokerGateway):
    async def get_info(self) -> Info | None:
        try:
            msg: RabbitMessage = await self.broker.request(
                message={},
                queue="get_info",
                timeout=TIMEOUT,
            )
        except TimeoutError:
            return None
        body = json.loads(msg.body)
        return Info(**body)
