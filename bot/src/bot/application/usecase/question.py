from bot.application.dto.pagination import PaginationDTO
from bot.application.dto.question import (
    AddQuestionDTO,
    GetQuestionDTO,
    AddQuestionIDDTO, GetQuestionListDTO,
)
from bot.application.interface.broker.gateway.question import (
    IQuestionBrokerGateway,
)
from bot.domain.service.question import QuestionService


class QuestionUseCase:
    def __init__(
            self,
            question_broker_gateway: IQuestionBrokerGateway,
            question_service: QuestionService,
    ) -> None:
        self.question_broker_gateway = question_broker_gateway
        self.question_service = question_service

    async def add(self, request: AddQuestionDTO) -> GetQuestionDTO:
        question = await self.question_broker_gateway.add_question(
            telegram_id=request.telegram_id,
            question=request.question,
        )
        data = self.question_service.get_question(question)
        return GetQuestionDTO(**data)

    async def get(self, request: AddQuestionIDDTO) -> GetQuestionDTO:
        question = await self.question_broker_gateway.get_question(
            question_id=request.question_id,
        )
        data = self.question_service.get_question(question)
        return GetQuestionDTO(**data)

    async def get_all(self, request: PaginationDTO) -> GetQuestionListDTO:
        question_list = await self.question_broker_gateway.get_question_list(
            limit=request.limit,
            offset=request.offset,
        )
        result = []
        for val in question_list.values:
            data = self.question_service.get_question(val)
            result.append(GetQuestionDTO(**data))
        return GetQuestionListDTO(
            total=question_list.total,
            limit=question_list.limit,
            offset=question_list.offset,
            values=result,
        )
