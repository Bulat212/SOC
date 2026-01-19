from aiogram import F, Router
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from dishka.integrations.aiogram import FromDishka, inject

from bot.application.dto.user import UserIDDTO
from bot.application.usecase.user import UserUseCase
from bot.domain.exception.info import InfoNotFound
from bot.domain.exception.user import UserNotFound
from bot.presentation.state.telegram import TelegramChannelState

telegram_router = Router()


@telegram_router.message(F.text.lower() == "telegram-канал")
@inject
async def send_telegram_channel(
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
    if user.role.lower() == "director":
        return
    try:
        await dialog_manager.start(
            state=TelegramChannelState.telegram_channel_url,
            mode=StartMode.NORMAL,
        )
    except InfoNotFound:
        return
