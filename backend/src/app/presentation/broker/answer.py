from dataclasses import asdict

from dishka import FromDishka
from dishka.integrations.faststream import inject
from faststream.rabbit import RabbitRouter, RabbitQueue

from app.application.dto.answer import AddAnswerDTO
from app.application.usecase.answer import AnswerUseCase
from app.presentation.schema.answer import AddAnswerSchema, GetAnswerSchema

answer_router = RabbitRouter()


@answer_router.subscriber(
    queue=RabbitQueue(
        name="add_answer",
        auto_delete=True,
    ),
)
@inject
async def add_answer(
        data: AddAnswerSchema,
        usecase: FromDishka[AnswerUseCase],
) -> GetAnswerSchema:
    request = AddAnswerDTO(**data.model_dump())
    answer = await usecase.add(request)
    return GetAnswerSchema(**asdict(answer))
