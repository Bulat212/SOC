import datetime
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput

from bot.constants import FORMAT_DATE
from bot.presentation.state.delegate import RegistrationDelegateState


async def set_last_name(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    text = message.text
    data = manager.start_data
    data["last_name"] = text
    await manager.switch_to(
        state=RegistrationDelegateState.first_name,
    )


async def set_first_name(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    text = message.text
    data = manager.start_data
    data["first_name"] = text
    await manager.switch_to(
        state=RegistrationDelegateState.patronymic,
    )


async def set_patronymic(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    text = message.text
    data = manager.start_data
    data["patronymic"] = text
    await manager.switch_to(
        state=RegistrationDelegateState.post,
    )


async def set_post(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    text = message.text
    data = manager.start_data
    data["post"] = text
    await manager.switch_to(
        state=RegistrationDelegateState.subject,
    )


async def set_subject(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    text = message.text
    data = manager.start_data
    data["subject"] = text
    await manager.switch_to(
        state=RegistrationDelegateState.start_date,
    )


async def set_start_work_date(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    text = message.text
    try:
        datetime.datetime.strptime(
            text or "",
            FORMAT_DATE,
        )
        manager.start_data["start_date"] = text
        await manager.switch_to(
            state=RegistrationDelegateState.end_date,
        )
        return
    except ValueError:
        await manager.switch_to(
            state=RegistrationDelegateState.invalid_start_date,
        )


async def set_end_work_date(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    text = message.text
    try:
        datetime.datetime.strptime(
            text or "",
            FORMAT_DATE,
        )
        manager.start_data["end_date"] = text
        await manager.switch_to(
            state=RegistrationDelegateState.finish,
        )
        return
    except ValueError:
        await manager.switch_to(
            state=RegistrationDelegateState.invalid_end_date,
        )