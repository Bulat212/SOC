from aiogram import Router, F
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from bot.presentation.state.delegate_data import DelegateDataState
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from bot.application.dto.user import UserIDDTO
from bot.application.usecase.user import UserUseCase
from bot.domain.exception.user import UserNotFound

delegate_data_router = Router()


@delegate_data_router.message(F.text.lower() == "мои данные")
@inject
async def my_data_handler(
        message: Message,
        dialog_manager: DialogManager,
        usecase: FromDishka[UserUseCase],
) -> None:
    await dialog_manager.reset_stack()
    request = UserIDDTO(
        telegram_id=str(message.from_user.id),
    )
    try:
        user = await usecase.get(request)
    except UserNotFound:
        return
    if user.role.lower() == "delegate":
        await dialog_manager.start(
            state=DelegateDataState.start,
            mode=StartMode.NORMAL,
            data={
                "telegram_id": str(message.from_user.id),
                "is_request": True,
            },
        )
    else:
        return
