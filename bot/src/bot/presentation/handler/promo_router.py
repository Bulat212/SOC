from aiogram import F, Router
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from bot.application.dto.user import UserIDDTO
from bot.application.usecase.user import UserUseCase
from bot.domain.exception.user import UserNotFound
from bot.presentation.state.promo import PromoState

promo_router = Router()


@promo_router.message(F.text.lower() == "промо")
@inject
async def promo_handler(
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
    await dialog_manager.start(
        state=PromoState.start,
        mode=StartMode.NORMAL,
        data={
            "role": user.role,
        },
    )
