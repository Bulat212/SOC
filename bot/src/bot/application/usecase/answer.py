from dataclasses import asdict

from bot.application.dto.answer import AddAnswerDTO
from bot.application.interface.broker.gateway.answer import (
    IAnswerBrokerGateway,
)
from bot.domain.service.answer import AnswerService


class AnswerUseCase:
    def __init__(
            self,
            answer_broker_gateway: IAnswerBrokerGateway,
            answer_service: AnswerService,
    ) -> None:
        self.answer_broker_gateway = answer_broker_gateway
        self.answer_service = answer_service

    async def add(self, request: AddAnswerDTO) -> None:
        answer = self.answer_service.add_answer(**asdict(request))
        await self.answer_broker_gateway.add_answer(answer)
