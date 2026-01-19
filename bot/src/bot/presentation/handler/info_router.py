from aiogram import Router, F
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from dishka import FromDishka
import logging
from bot.application.dto.user import UserIDDTO
from bot.application.usecase.user import UserUseCase
from bot.domain.exception.user import UserNotFound
from bot.presentation.state.info import InfoState

info_router = Router()


@info_router.message(F.text.lower() == "ℹ️ инфо")
async def info_handler(
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
    if user.role not in ("candidate", "delegate"):
        return
    logging.debug("НОВЫЙ ДИАЛОГ")
    await dialog_manager.start(
        state=InfoState.start,
        mode=StartMode.NORMAL,
        data={
            "role": user.role,
        },
    )
