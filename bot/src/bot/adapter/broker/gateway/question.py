import json

from faststream.rabbit.message import RabbitMessage

from bot.adapter.broker.gateway.base import BaseBrokerGateway
from bot.constants import TIMEOUT, ZERO
from bot.domain.model.question import Question, QuestionList


class QuestionBrokerGateway(BaseBrokerGateway):
    async def add_question(self,
            telegram_id: str,
            question: str,
    ) -> Question | None:
        try:
            msg: RabbitMessage = await self.broker.request(
                message={
                    "telegram_id": telegram_id,
                    "question": question,
                },
                queue="add_question",
                timeout=TIMEOUT,
            )
        except TimeoutError:
            return None
        body = json.loads(msg.body)
        return Question(**body)

    async def get_question(self, question_id: str) -> Question | None:
        try:
            msg: RabbitMessage = await self.broker.request(
                message={
                    "question_id": question_id,
                },
                queue="get_question",
                timeout=TIMEOUT,
            )
        except TimeoutError:
            return None
        body = json.loads(msg.body)
        return Question(**body)

    async def get_question_list(
            self,
            limit: int,
            offset: int,
    ) -> QuestionList:
        try:
            msg: RabbitMessage = await self.broker.request(
                message={
                    "limit": limit,
                    "offset": offset,
                },
                queue="get_question_list",
                timeout=TIMEOUT,
            )
        except TimeoutError:
            return QuestionList(
                total=ZERO,
                limit=limit,
                offset=offset,
                values=[],
            )
        body = json.loads(msg.body)

        return QuestionList(
            limit=limit,
            offset=offset,
            total=body.get("total"),
            values=[
                Question(**val) for val in body.get("values")
            ],
        )
