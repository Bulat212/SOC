from dataclasses import asdict

from dishka import FromDishka
from dishka.integrations.faststream import inject
from faststream.rabbit import RabbitRouter, RabbitQueue

from app.application.dto.faq import AddFaqIDDTO, AddFaqDTO
from app.application.dto.pagination import PaginationDTO
from app.application.usecase.faq import FaqUseCase
from app.presentation.schema.faq import (
    AddFaqIDSchema,
    GetFaqSchema,
    GetFaqListSchema,
    AddFaqSchema,
)
from app.presentation.schema.pagination import PaginationSchema

faq_router = RabbitRouter()


@faq_router.subscriber(
    queue=RabbitQueue(
        "get_faq",
        auto_delete=True,
    ),
)
@inject
async def get_faq(
        data: AddFaqIDSchema,
        usecase: FromDishka[FaqUseCase],
) -> GetFaqSchema:
    request = AddFaqIDDTO(**data.model_dump())
    faq = await usecase.get(request)
    return GetFaqSchema(**asdict(faq))


@faq_router.subscriber(
    queue=RabbitQueue(
        "get_faq_list",
        auto_delete=True,
    ),
)
@inject
async def get_faq_list(
        data: PaginationSchema,
        usecase: FromDishka[FaqUseCase],
) -> GetFaqListSchema:
    request = PaginationDTO(**data.model_dump())
    faq_list = await usecase.all(request)
    result = []
    for faq in faq_list.values:
        result.append(GetFaqSchema(**asdict(faq)))
    return GetFaqListSchema(
        total=faq_list.total,
        limit=faq_list.limit,
        offset=faq_list.offset,
        values=result,
    )


@faq_router.subscriber(
    queue=RabbitQueue(
        "add_faq",
        auto_delete=True,
    ),
)
@inject
async def add_faq(
        data: AddFaqSchema,
        usecase: FromDishka[FaqUseCase],
) -> GetFaqSchema:
    request = AddFaqDTO(**data.model_dump())
    faq = await usecase.add(request)
    return GetFaqSchema(**asdict(faq))


@faq_router.subscriber(
    queue=RabbitQueue(
        "delete_faq",
        auto_delete=True,
    ),
)
@inject
async def delete_faq(
        data: AddFaqIDSchema,
        usecase: FromDishka[FaqUseCase],
) -> None:
    request = AddFaqIDDTO(**data.model_dump())
    await usecase.delete(request)
