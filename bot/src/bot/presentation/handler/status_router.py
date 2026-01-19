from aiogram import Router, F
from aiogram.types import Message
from aiogram_dialog import DialogManager
from dishka import FromDishka

from bot.application.dto.user import UserIDDTO
from bot.application.usecase.user import UserUseCase
from bot.domain.exception.status import StatusNotFound
from bot.domain.exception.user import UserNotFound
from bot.presentation.state.status import StatusState

status_router = Router()


@status_router.message(F.text.lower() == "🔍 статус заявки")
async def status_handler(
        message: Message,
        dialog_manager: DialogManager,
        usecase: FromDishka[UserUseCase],
) -> None:
    request = UserIDDTO(
        telegram_id=str(message.from_user.id),
    )
    try:
        user = await usecase.get(request)
    except UserNotFound:
        return

    match user.role.lower():
        case "candidate":
            try:
                await dialog_manager.start(
                    state=StatusState.status,
                    data={
                        "user_id": message.from_user.id,
                    },
                )
            except StatusNotFound:
                return
        case _:
            return
