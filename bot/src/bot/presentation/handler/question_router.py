from aiogram import Router, F
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from bot.application.dto.user import UserIDDTO
from bot.application.usecase.user import UserUseCase
from bot.constants import LIMIT_QUESTION, ZERO
from bot.domain.exception.user import UserNotFound
from bot.presentation.state.question import QuestionState

question_router = Router()


@question_router.message(F.text.lower() == "❓ задать вопрос")
@inject
async def ask_question_handler(
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
    if not user.role == "candidate":
        return
    await dialog_manager.start(
        state=QuestionState.start,
        mode=StartMode.NORMAL,
        data={
            "user_id": message.from_user.id,
        },
    )


@question_router.message(F.text.lower() == "входящие вопросы")
@inject
async def incoming_questions(
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
    if not user.role == "director":
        return
    await dialog_manager.start(
        state=QuestionState.question_list,
        mode=StartMode.NORMAL,
        data={
            "limit": LIMIT_QUESTION,
            "offset": ZERO,
        }
    )
