from aiogram import Router, F
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from bot.application.dto.user import UserIDDTO
from bot.application.usecase.user import UserUseCase
from bot.domain.exception.user import UserNotFound

from bot.presentation.state.get_candidate import GetCandidateState

get_candidate_router = Router()

@get_candidate_router.message(F.text.lower() == "список кандидатов")
@inject
async def get_candidate_handler(
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
        state=GetCandidateState.recruitment,
        mode=StartMode.NORMAL,
        data={"role": "director"},
    )
