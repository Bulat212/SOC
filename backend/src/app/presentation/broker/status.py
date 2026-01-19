from dataclasses import asdict

from dishka import FromDishka
from dishka.integrations.faststream import inject
from faststream.rabbit import RabbitRouter, RabbitQueue

from app.application.dto.candidate import AddCandidateIDDTO
from app.application.usecase.status import StatusUseCase
from app.presentation.schema.candidate import AddCandidateIDSchema
from app.presentation.schema.status import GetStatusSchema

status_router = RabbitRouter()


@status_router.subscriber(
    queue=RabbitQueue(
        "get_status",
        auto_delete=True,
    ),
)
@inject
async def get_status(
        data: AddCandidateIDSchema,
        usecase: FromDishka[StatusUseCase],
) -> GetStatusSchema:
    request = AddCandidateIDDTO(
        telegram_id=data.telegram_id,
        id=data.id,
    )
    status = await usecase.get(request)
    return GetStatusSchema(**asdict(status))
