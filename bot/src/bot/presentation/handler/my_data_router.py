from aiogram import Router, F
from aiogram.types import Message, URLInputFile
from aiogram_dialog import DialogManager, StartMode
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from bot.application.dto.user import UserIDDTO
from bot.application.usecase.user import UserUseCase
from bot.domain.exception.user import UserNotFound
from bot.presentation.state.my_data import MyDataState
from bot.presentation.state.my_form import MyDocumentState
from bot.presentation.state.delegate_data import DelegateDataState

my_data_router = Router()


@my_data_router.message(F.text.lower() == "👤 мои данные")
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
    # if user.role.lower() in ["director", "delegate"]:
    #     return
    if user.role.lower() == "director":
        return
    
    if user.role.lower() == "candidate":
        await dialog_manager.start(
            state=MyDataState.start,
            mode=StartMode.NORMAL,
            data={
                "telegram_id": str(message.from_user.id),
                "is_request": True,
            },
        )
    elif user.role.lower() == "delegate":
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


@my_data_router.message(F.text.lower() == "📁 мои документы")
@inject
async def my_document_handler(
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
    if user.role.lower() in ["director", "delegate"]:
        return
    await dialog_manager.start(
        state=MyDocumentState.document,
        mode=StartMode.NORMAL,
        data={
            "user_id": str(message.from_user.id),
        },
    )
