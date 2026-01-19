from dishka.integrations.faststream import FromDishka, inject
from faststream.rabbit import RabbitRouter, RabbitQueue

from app.application.dto.user import GetUserIDDTO
from app.application.usecase.user import UserUseCase
from app.presentation.schema.user import (
    DeleteUserSchema,
    GetUserSchema,
    GetUserIDSchema,
    GetUsersIDSchema,
)

user_router = RabbitRouter()


@user_router.subscriber(
    queue=RabbitQueue(
        "get_user",
        auto_delete=True,
    ),
)
@inject
async def get_user(
        data: GetUserIDSchema,
        usecase: FromDishka[UserUseCase],
) -> GetUserSchema | None:
    request = GetUserIDDTO(**data.model_dump())
    user = await usecase.get(request)
    return GetUserSchema(
        id=user.id,
        telegram_id=user.telegram_id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role,
        is_active=user.is_active,
    )


@user_router.subscriber(
    queue=RabbitQueue(
        "get_users_director_id",
        auto_delete=True,
    ),
)
@inject
async def get_users_director_id(
        usecase: FromDishka[UserUseCase],
) -> GetUsersIDSchema:
    user_id_list = await usecase.get_director_id_all()
    return GetUsersIDSchema(
        values=[
            GetUserIDSchema(
                telegram_id=val.telegram_id,
                id=None,
            )
            for val in user_id_list.values
        ],
    )


@user_router.subscriber(
    queue=RabbitQueue(
        "delete_user",
        auto_delete=True,
    ),
)
@inject
async def delete_user(
        data: DeleteUserSchema,
        usecase: FromDishka[UserUseCase],
):
    user_id = data.user_id
    await usecase.delete_user(user_id)
