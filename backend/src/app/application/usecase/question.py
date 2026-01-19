from app.application.dto.pagination import PaginationDTO
from app.application.dto.question import (
    AddQuestionDTO,
    GetQuestionDTO,
    AddQuestionIDDTO,
    GetQuestionListDTO,
)
from app.application.interface.db import DBSession
from app.application.interface.gateway.question import IQuestionDBGateway
from app.application.interface.gateway.user import IUserDBGateway
from app.application.interface.ulid_generator import ULIDGenerator
from app.domain.service.question import QuestionService
from app.domain.service.user import UserService


class QuestionUseCase:
    def __init__(
            self,
            question_db_gateway: IQuestionDBGateway,
            user_db_gateway: IUserDBGateway,
            db_session: DBSession,
            question_service: QuestionService,
            user_service: UserService,
            ulid_generator: ULIDGenerator,
    ) -> None:
        self.question_db_gateway = question_db_gateway
        self.user_db_gateway = user_db_gateway
        self.db_session = db_session
        self.question_service = question_service
        self.user_service = user_service
        self.ulid_generator = ulid_generator

    async def add(self, request: AddQuestionDTO) -> GetQuestionDTO:
        user = await self.user_db_gateway.get(
            user_id=request.user_id,
            telegram_id=request.telegram_id,
        )
        user_id = self.user_service.get_user_telegram_id(user)
        number = await self.question_db_gateway.get_number()
        number = self.question_service.get_number(number)

        question = self.question_service.add_question(
            id=str(self.ulid_generator()),
            user_id=user_id,
            question=request.question,
            number=number,
        )
        question = await self.question_db_gateway.insert(question)
        data = self.question_service.get_question(question)
        await self.db_session.commit()
        return GetQuestionDTO(**data)

    async def get(self, request: AddQuestionIDDTO) -> GetQuestionDTO:
        question = await self.question_db_gateway.get(
            question_id=request.question_id,
        )
        data = self.question_service.get_question(question)
        return GetQuestionDTO(**data)

    async def get_all(self, request: PaginationDTO) -> GetQuestionListDTO:
        question_list = self.question_db_gateway.all(
            limit=request.limit,
            offset=request.offset * request.limit,
        )
        total = await self.question_db_gateway.get_total()
        result = []
        async for val in question_list:
            data = self.question_service.get_question(val)
            result.append(GetQuestionDTO(**data))
        return GetQuestionListDTO(
            total=total,
            limit=request.limit,
            offset=request.offset,
            values=result,
        )
