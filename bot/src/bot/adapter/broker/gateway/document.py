import json

from faststream.rabbit.message import RabbitMessage

from bot.adapter.broker.gateway.base import BaseBrokerGateway
from bot.constants import TIMEOUT
from bot.domain.model.document import Document


class DocumentBrokerGateway(BaseBrokerGateway):
    async def get_document(self, name: str) -> Document | None:
        try:
            msg: RabbitMessage = await self.broker.request(
                message={
                    "name": name,
                },
                queue="get_document",
                timeout=TIMEOUT,
            )
        except TimeoutError:
            return None
        data = json.loads(msg.body)
        return Document(**data)
