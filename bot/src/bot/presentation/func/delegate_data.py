import datetime

from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from bot.constants import FORMAT_DATE
from bot.presentation.state.delegate_data import DelegateDataState


async def set_first_name(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    text = message.text
    manager.start_data["first_name"] = text
    manager.start_data["is_save"] = True
    await message.answer(
        text="Ваше имя изменено.",
    )
    await manager.switch_to(
        state=DelegateDataState.start,
    )


async def set_patronymic(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    text = message.text
    manager.start_data["patronymic"] = text
    manager.start_data["is_save"] = True
    await message.answer(
        text="Ваше отчество изменено.",
    )
    await manager.switch_to(
        state=DelegateDataState.start,
    )


async def set_last_name(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    text = message.text
    manager.start_data["last_name"] = text
    manager.start_data["is_save"] = True
    await message.answer(
        text="Ваша фамилия изменена",
    )
    await manager.switch_to(
        state=DelegateDataState.start,
    )


async def set_subject(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    text = message.text
    manager.start_data["subject"] = text
    manager.start_data["is_save"] = True
    await message.answer(
        text="Ваш субъект изменен",
    )
    await manager.switch_to(
        state=DelegateDataState.start,
    )


async def set_post(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    text = message.text
    manager.start_data["post"] = text
    manager.start_data["is_save"] = True
    await message.answer(
        text="Ваша должность изменена",
    )
    await manager.switch_to(
        state=DelegateDataState.start,
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
        manager.start_data["is_save"] = True
        await manager.switch_to(
            state=DelegateDataState.start,
        )
        return
    except ValueError:
        await manager.switch_to(
            state=DelegateDataState.invalid_start_date,
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
        manager.start_data["is_save"] = True
        await manager.switch_to(
            state=DelegateDataState.start,
        )
        return
    except ValueError:
        await manager.switch_to(
            state=DelegateDataState.invalid_end_date,
        )
