import json

from faststream.rabbit.message import RabbitMessage

from bot.adapter.broker.gateway.base import BaseBrokerGateway
from bot.constants import TIMEOUT
from bot.domain.model.recruitmet import Recruitment


class RecruitmentBrokerGateway(BaseBrokerGateway):
    async def get_recruitments(self) -> list[Recruitment]:
        try:
            msg: RabbitMessage = await self.broker.request(
                message={},
                queue="get_recruitments",
                timeout=TIMEOUT,
            )
        except TimeoutError:
            return []
        body = json.loads(msg.body)
        result = []
        for val in body.get("values"):
            result.append(Recruitment(**val))
        return result

    async def get_recruitment(self,
            recruitment_id: str,
    ) -> Recruitment | None:
        try:
            msg: RabbitMessage = await self.broker.request(
                message={
                    "id": recruitment_id,
                },
                queue="get_recruitment",
                timeout=TIMEOUT,
            )
        except TimeoutError:
            return None
        body = json.loads(msg.body)
        return Recruitment(**body)
