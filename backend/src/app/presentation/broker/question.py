from dataclasses import asdict

from dishka import FromDishka
from dishka.integrations.faststream import inject
from faststream.rabbit import RabbitRouter, RabbitQueue

from app.application.dto.pagination import PaginationDTO
from app.application.dto.question import AddQuestionDTO, AddQuestionIDDTO
from app.application.usecase.question import QuestionUseCase
from app.presentation.schema.pagination import PaginationSchema
from app.presentation.schema.question import (
    AddQuestionSchema,
    GetQuestionSchema,
    AddQuestionIDSchema,
    GetQuestionListSchema,
)

question_router = RabbitRouter()


@question_router.subscriber(
    queue=RabbitQueue(
        "add_question",
        auto_delete=True,
    ),
)
@inject
async def add_question(
        data: AddQuestionSchema,
        usecase: FromDishka[QuestionUseCase],
) -> GetQuestionSchema:
    request = AddQuestionDTO(**data.model_dump())
    question = await usecase.add(request)
    return GetQuestionSchema(**asdict(question))


@question_router.subscriber(
    queue=RabbitQueue(
        "get_question",
        auto_delete=True,
    ),
)
@inject
async def get_question(
        data: AddQuestionIDSchema,
        usecase: FromDishka[QuestionUseCase],
) -> GetQuestionSchema:
    request = AddQuestionIDDTO(**data.model_dump())
    question = await usecase.get(request)
    return GetQuestionSchema(**asdict(question))


@question_router.subscriber(
    queue=RabbitQueue(
        "get_question_list",
        auto_delete=True,
    ),
)
@inject
async def get_question_list(
        data: PaginationSchema,
        usecase: FromDishka[QuestionUseCase],
) -> GetQuestionListSchema:
    request = PaginationDTO(**data.model_dump())
    question_list = await usecase.get_all(request)
    return GetQuestionListSchema(
        limit=question_list.limit,
        offset=question_list.offset,
        total=question_list.total,
        values=[
            GetQuestionSchema(**asdict(val))
            for val in question_list.values
        ],
    )
