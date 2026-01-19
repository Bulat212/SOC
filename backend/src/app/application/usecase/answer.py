from dataclasses import asdict

from app.application.dto.answer import AddAnswerDTO, GetAnswerDTO, AnswerIDDTO
from app.application.interface.db import DBSession
from app.application.interface.gateway.answer import IAnswerDBGateway
from app.application.interface.gateway.question import IQuestionDBGateway
from app.application.interface.ulid_generator import ULIDGenerator
from app.domain.service.answer import AnswerService


class AnswerUseCase:
    def __init__(
            self,
            answer_db_gateway: IAnswerDBGateway,
            question_db_gateway: IQuestionDBGateway,
            ulid_generator: ULIDGenerator,
            db_session: DBSession,
            service: AnswerService,
    ) -> None:
        self.answer_db_gateway = answer_db_gateway
        self.question_db_gateway = question_db_gateway
        self.ulid_generator = ulid_generator
        self.db_session = db_session
        self.service = service

    async def add(self, request: AddAnswerDTO) -> GetAnswerDTO:
        answer = self.service.add_answer(
            **asdict(request),
            id=str(self.ulid_generator()),
        )
        answer = await self.answer_db_gateway.insert(
            answer=answer,
        )
        await self.question_db_gateway.change_status(
            question_id=request.question_id,
            is_answer=True,
        )
        await self.db_session.commit()
        data = self.service.get_answer(answer)
        return GetAnswerDTO(**data)

    async def get(self, request: AnswerIDDTO) -> GetAnswerDTO:
        answer = await self.answer_db_gateway.get(answer_id=request.id)
        data = self.service.get_answer(answer)
        return GetAnswerDTO(**data)
