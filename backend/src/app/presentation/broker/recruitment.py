from dataclasses import asdict

from dishka.integrations.faststream import FromDishka, inject
from faststream.rabbit import RabbitRouter, RabbitQueue

from app.application.dto.recruitment import AddRecruitmentIDDTO
from app.application.usecase.recruitment import RecruitmentUseCase
from app.presentation.schema.recruitment import (
    GetRecruitmentsSchema,
    GetRecruitmentSchema,
    AddRecruitmentIDSchema,
)

recruitment_router = RabbitRouter()


@recruitment_router.subscriber(
    queue=RabbitQueue(
        "get_recruitments",
        auto_delete=True,
    ),
)
@inject
async def get_recruitments(
        usecase: FromDishka[RecruitmentUseCase],
) -> GetRecruitmentsSchema:
    recruitments = await usecase.get_all()
    result = []
    for val in recruitments.values:
        result.append(GetRecruitmentSchema(**asdict(val)))
    return GetRecruitmentsSchema(
        values=result,
    )


@recruitment_router.subscriber(
    queue=RabbitQueue(
        "get_recruitment",
        auto_delete=True,
    ),
)
@inject
async def get_recruitment(
        data: AddRecruitmentIDSchema,
        usecase: FromDishka[RecruitmentUseCase],
) -> GetRecruitmentSchema:
    request = AddRecruitmentIDDTO(
        id=data.id,
    )
    recruitment = await usecase.get(request)
    return GetRecruitmentSchema(**asdict(recruitment))
