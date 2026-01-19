from aiogram import Router, F
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from bot.application.dto.user import UserIDDTO
from bot.application.usecase.user import UserUseCase
from bot.constants import LIMIT_FAQ, ZERO
from bot.domain.exception.faq import FaqNotFound
from bot.domain.exception.user import UserNotFound
from bot.presentation.state.faq import FaqState

faq_router = Router()


@faq_router.message(F.text.lower() == "faq")
@inject
async def faq_handler(
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
    try:
        await dialog_manager.start(
            state=FaqState.faq,
            mode=StartMode.NORMAL,
            data={
                "limit": LIMIT_FAQ,
                "offset": ZERO,
                "role": user.role,
            },
        )
    except FaqNotFound:
        return