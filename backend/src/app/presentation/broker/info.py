from dataclasses import asdict

from dishka import FromDishka
from dishka.integrations.faststream import inject
from faststream.rabbit import RabbitRouter, RabbitQueue

from app.application.usecase.info import InfoUseCase
from app.presentation.schema.info import GetInfoSchema

info_router = RabbitRouter()


@info_router.subscriber(
    queue=RabbitQueue(
        "get_info",
        auto_delete=True,
    ),
)
@inject
async def get_info(
        usecase: FromDishka[InfoUseCase],
) -> GetInfoSchema:
    info = await usecase.get()
    return GetInfoSchema(**asdict(info))
