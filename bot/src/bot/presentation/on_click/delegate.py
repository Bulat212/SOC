from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button

from bot.presentation.state.delegate import RegistrationDelegateState

from dataclasses import asdict
from typing import Any

from aiogram_dialog.api.entities import Context
from bot.application.dto.delegate import AddDelegateDTO, DelegateIDDTO
from bot.application.dto.user import UserIDDTO
from bot.application.usecase.delegate import DelegateUseCase
from bot.application.usecase.user import UserUseCase
from bot.presentation.button.start_button import StartDelegateKeyboardButton
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from aiogram_dialog import DialogManager
import datetime
from aiogram.types import Message




async def start_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=RegistrationDelegateState.last_name,
    )


async def skip_subject(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=RegistrationDelegateState.start_date,
        show_mode=ShowMode.SEND,
    )


async def skip_start_work_date(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=RegistrationDelegateState.end_date,
        show_mode=ShowMode.SEND,
    )


async def skip_end_work_date(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=RegistrationDelegateState.finish,
        show_mode=ShowMode.SEND,
    )


@inject
async def start_delegate(
    cq: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
    delegate_usecase: FromDishka[DelegateUseCase],
    user_usecase: FromDishka[UserUseCase],
    **kwargs,
):
    data = dialog_manager.start_data
    telegram_id = data.get("user_id")

    request = UserIDDTO(telegram_id=str(telegram_id))
    user = await user_usecase.get(request)

    start_date = data.get("start_date")
    end_date = data.get("end_date")

    format_start_date = (
        datetime.datetime.strptime(start_date, "%d.%m.%Y").date()
        if start_date else None
    )
    format_end_date = (
        datetime.datetime.strptime(end_date, "%d.%m.%Y").date()
        if end_date else None
    )

    delegate = AddDelegateDTO(
        user_id=user.id,
        telegram_id=str(telegram_id),
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        patronymic=data.get("patronymic"),
        post=data.get("post"),
        subject=data.get("subject"),
        start_date=format_start_date,
        end_date=format_end_date,
    )

    await delegate_usecase.add_delegate(delegate)

    keyboard = StartDelegateKeyboardButton(
        resize_keyboard=True,
        one_time_keyboard=False,
        is_persistent=True,
    )

    await cq.message.answer(
        text="Выберите интересующий вас раздел.",
        reply_markup=keyboard(),
    )