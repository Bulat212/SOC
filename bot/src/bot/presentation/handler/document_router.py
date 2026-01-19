from aiogram import F, Router
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from dishka.integrations.aiogram import FromDishka, inject

from bot.application.dto.user import UserIDDTO
from bot.application.usecase.user import UserUseCase
from bot.domain.exception.info import InfoNotFound
from bot.domain.exception.user import UserNotFound
from bot.presentation.state.document import DocumentState

document_router = Router()


@document_router.message(F.text.lower() == "руководящие документы")
@inject
async def guarding_document_handler(
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
    # if user.role.lower() == "director":
    #     return

    try:
        await dialog_manager.start(
            state=DocumentState.start_guarding,
            mode=StartMode.NORMAL,
        )
    except InfoNotFound:
        return


@document_router.message(F.text.lower() == "образцы документов кандидата")
@inject
async def candidate_document_handler(
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
            state=DocumentState.start,
            mode=StartMode.NORMAL,
        )
    except InfoNotFound:
        return
