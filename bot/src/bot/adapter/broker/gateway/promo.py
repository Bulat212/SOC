import json

from faststream.rabbit.message import RabbitMessage

from bot.adapter.broker.gateway.base import BaseBrokerGateway
from bot.constants import TIMEOUT
from bot.domain.model.document import PromoDocument


class PromoBrokerGateway(BaseBrokerGateway):
    async def get_promo_document(self, name: str) -> PromoDocument | None:
        try:
            msg: RabbitMessage = await self.broker.request(
                message={
                    "name": name,
                },
                queue="get_promo_document",
                timeout=TIMEOUT,
            )
        except TimeoutError:
            return None
        data = json.loads(msg.body)
        return PromoDocument(**data)

    async def delete_promo_document(self, name: str) -> None:
        await self.broker.publish(
            message={
                "name": name,
            },
            queue="delete_promo_document",
        )

    async def get_promo_documents_name(self) -> list[str]:
        try:
            msg: RabbitMessage = await self.broker.request(
                message={},
                queue="get_promo_documents_name",
                timeout=TIMEOUT,
            )
        except TimeoutError:
            return []
        data = json.loads(msg.body)
        result = []
        for val in data.get("values"):
            result.append(val.get("name"))
        return result

    async def add_promo_document(
            self,
            name: str,
            file: str,
            filename: str,
    ) -> None:
        await self.broker.publish(
            message={
                "name": name,
                "file": file,
                "filename": filename,
            },
            queue="add_promo_document",
        )
