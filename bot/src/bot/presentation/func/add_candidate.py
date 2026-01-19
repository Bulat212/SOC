import asyncio
import datetime
import re

from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput

from bot.constants import FORMAT_BIRTHDATE, MIN_AGE, MAX_AGE
from bot.presentation.state.add_candidate import AddCandidateState


async def set_graduation_data(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    text = message.text
    try:
        datetime.datetime.strptime(
            text or "",
            FORMAT_BIRTHDATE,
        )
        manager.start_data["graduation_date"] = text
        await manager.switch_to(
            state=AddCandidateState.direction_training,
        )
        return
    except ValueError:
        await manager.switch_to(
            state=AddCandidateState.invalid_graduation_date,
        )


async def set_birthdate(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    text = message.text
    try:
        birthdate = datetime.datetime.strptime(
            text or "",
            FORMAT_BIRTHDATE,
        )
        today = datetime.date.today()
        age = today.year - birthdate.year - (
                (today.month, today.day) < (birthdate.month, birthdate.day)
        )
        if MIN_AGE > age or MAX_AGE < age:
            await manager.switch_to(
                state=AddCandidateState.invalid_period_birthdate,
            )
            # await manager.done()
            asyncio.create_task(manager.reset_stack())
            return
        manager.start_data["birthdate"] = text
        await manager.switch_to(
            state=AddCandidateState.subject,
        )
    except ValueError:
        await manager.switch_to(
            state=AddCandidateState.invalid_birthdate,
        )
        return

async def set_subject(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    text = message.text
    manager.start_data["subject"] = text
    await manager.switch_to(
        state=AddCandidateState.last_name,
    )


async def set_last_name(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    text = message.text
    data = manager.start_data
    data["last_name"] = text
    await manager.switch_to(
        state=AddCandidateState.first_name,
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
        state=AddCandidateState.patronymic,
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
        state=AddCandidateState.military_station,
    )


async def set_military_station(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    text = message.text
    data = manager.start_data
    data["military_station"] = text
    await manager.switch_to(
        state=AddCandidateState.military_station_address,
    )


async def set_military_station_address(
        message: Message,
        manage_input: MessageInput,
        manager: DialogManager,
) -> None:
    text = message.text
    data = manager.start_data
    data["military_station_address"] = text
    await manager.switch_to(
        state=AddCandidateState.university,
    )


async def set_university(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    text = message.text
    data = manager.start_data
    data["university"] = text
    await manager.switch_to(
        state=AddCandidateState.graduation_date,
    )


async def set_direction_training(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    text = message.text
    manager.start_data["direction_training"] = text
    await manager.switch_to(
        state=AddCandidateState.average_score,
    )


async def set_average_score(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    text = message.text
    try:
        score = float(text.replace(",", "."))
        manager.start_data["average_score"] = score
    except ValueError:
        await manager.switch_to(
            state=AddCandidateState.invalid_average_score,
        )
        return
    if score < 4:
        await manager.switch_to(
            state=AddCandidateState.low_average_score,
        )
        await manager.done()
        return
    elif score > 5:
        await manager.switch_to(
            state=AddCandidateState.invalid_average_score,
        )
        return
    await manager.switch_to(
        state=AddCandidateState.find_out,
    )


async def set_find_out(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    text = message.text
    manager.start_data["find_out"] = text
    manager.show_mode = ShowMode.SEND
    await manager.switch_to(
        state=AddCandidateState.phone_number,
        show_mode=ShowMode.SEND,
    )

PHONE_REGEX = re.compile(r'^\+?\d{10,15}$')

async def set_phone_number(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    phone_number = None

    if message.contact and message.contact.phone_number:
        phone_number = message.contact.phone_number
    elif message.text:
        text = message.text.strip()
        if PHONE_REGEX.match(text): 
            phone_number = text

    if phone_number:
        manager.start_data["phone_number"] = phone_number
        await manager.switch_to(AddCandidateState.recruitment)
        return

    await manager.switch_to(AddCandidateState.invalid_phone_number)