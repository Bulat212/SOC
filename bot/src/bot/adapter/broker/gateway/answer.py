from bot.adapter.broker.gateway.base import BaseBrokerGateway
from bot.domain.model.answer import Answer


class AnswerBrokerGateway(BaseBrokerGateway):
    async def add_answer(self, answer: Answer) -> None:
        await self.broker.publish(
            message={
                "question_id": answer.question_id,
                "answer": answer.answer,
            },
            queue="add_answer",
        )
