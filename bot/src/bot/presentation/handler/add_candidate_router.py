from aiogram import Router, F
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from bot.application.dto.user import UserIDDTO #AddUserIDDTO
from bot.application.usecase.user import UserUseCase
from bot.constants import LIMIT_FAQ, ZERO
from bot.domain.exception.faq import FaqNotFound
from bot.domain.exception.user import UserNotFound
from bot.presentation.state.add_candidate import AddCandidateState

add_candidate_router = Router()


@add_candidate_router.message(F.text.lower() == "добавить кандидатаfffff")
@inject
async def add_candidate_handler(
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
            state=AddCandidateState.start,
            mode=StartMode.NORMAL,
            data={
                "role": user.role,
            },
        )
        #изменить
    except FaqNotFound:
        return
