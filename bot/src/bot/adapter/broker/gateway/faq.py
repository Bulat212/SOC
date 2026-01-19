import json

from faststream.rabbit.message import RabbitMessage

from bot.adapter.broker.gateway.base import BaseBrokerGateway
from bot.constants import TIMEOUT
from bot.domain.model.faq import Faq, FaqList


class FaqBrokerGateway(BaseBrokerGateway):
    async def get_faq(self, faq_id: str) -> Faq | None:
        try:
            msg: RabbitMessage = await self.broker.request(
                message={
                    "id": faq_id,
                },
                queue="get_faq",
                timeout=TIMEOUT,
            )
        except TimeoutError:
            return None
        data = json.loads(msg.body)
        return Faq(**data)

    async def get_faq_list(self, limit: int, offset: int) -> FaqList | None:
        try:
            msg: RabbitMessage = await self.broker.request(
                message={
                    "limit": limit,
                    "offset": offset,
                },
                queue="get_faq_list",
                timeout=TIMEOUT,
            )
        except TimeoutError:
            return
        data = json.loads(msg.body)
        result = []
        for val in data.get("values"):
            result.append(Faq(**val))
        return FaqList(
            total=data.get("total"),
            limit=data.get("limit"),
            offset=data.get("offset"),
            values=result,
        )

    async def add_faq(self, faq: Faq) -> None:
        await self.broker.publish(
            message={
                "question": faq.question,
                "answer": faq.answer,
            },
            queue="add_faq",
        )

    async def delete_faq(self, faq_id: str) -> None:
        await self.broker.publish(
            message={
                "id": faq_id,
            },
            queue="delete_faq"
        )
