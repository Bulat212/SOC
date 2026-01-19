from dataclasses import asdict
from dishka.integrations.faststream import FromDishka, inject
from faststream.rabbit import RabbitRouter, RabbitQueue

from app.application.dto.delegate import AddDelegateDTO, GetDelegateIDDTO, UpdateDelegateDTO
from app.application.usecase.delegate import DelegateUseCase

from app.presentation.schema.delegate import AddDelegateSchema, GetDelegateIDSchema, GetDelegateSchema, UpdateDelegateSchema

delegate_router = RabbitRouter()


@delegate_router.subscriber(
    queue=RabbitQueue(
        "get_delegate",
        auto_delete=True,
    ),
)
@inject
async def get_delegate(
        data: GetDelegateIDSchema,
        usecase: FromDishka[DelegateUseCase],
) -> GetDelegateSchema | None:
    request = GetDelegateIDDTO(**data.model_dump())
    delegate = await usecase.get(request)
    return GetDelegateSchema(
        id=delegate.id,
        telegram_id=delegate.telegram_id,
        user_id=delegate.user_id,
        first_name=delegate.first_name,
        last_name=delegate.last_name,
        patronymic=delegate.patronymic,
        post=delegate.post,
        subject=delegate.subject,
        start_date=delegate.start_date,
        end_date=delegate.end_date,
    )

@delegate_router.subscriber("update_delegate")
@inject
async def update_delegate(
        data: UpdateDelegateSchema,
        usecase: FromDishka[DelegateUseCase],
) -> GetDelegateSchema:
    request = UpdateDelegateDTO(**data.model_dump())

    delegate = await usecase.update(request)
    return GetDelegateSchema(**asdict(delegate))


@delegate_router.subscriber(
    queue=RabbitQueue(
        "add_delegate",
        auto_delete=True,
    ),
)
@inject
async def add_delegate(
        data: AddDelegateSchema,
        usecase: FromDishka[DelegateUseCase],
) -> GetDelegateSchema:
    request = AddDelegateDTO(**data.model_dump())
    delegate = await usecase.add(request)
    return GetDelegateSchema(**asdict(delegate))
