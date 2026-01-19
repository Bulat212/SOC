import datetime

from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from bot.constants import MAX_AGE, MIN_AGE, FORMAT_BIRTHDATE
from bot.presentation.button.start_button import StartCandidateKeyboardButton
from bot.presentation.state.my_data import MyDataState


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
        manager.start_data["is_save"] = True
        await manager.switch_to(
            state=MyDataState.start,
        )
        return
    except ValueError:
        await manager.switch_to(
            state=MyDataState.invalid_graduation_date,
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
                state=MyDataState.invalid_period_birthdate,
            )
            return
        manager.start_data["birthdate"] = text
        manager.start_data["is_save"] = True
        await message.answer(
            text="Ваша дата рождения изменена.",
        )
        await manager.switch_to(
            state=MyDataState.start,
        )
    except ValueError:
        await manager.switch_to(
            state=MyDataState.invalid_birthdate,
        )
        return


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
        state=MyDataState.start,
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
        state=MyDataState.start,
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
        state=MyDataState.start,
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
        text="Ваш город изменен",
    )
    await manager.switch_to(
        state=MyDataState.start,
    )


async def set_military_station(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    text = message.text
    manager.start_data["military_station"] = text
    manager.start_data["is_save"] = True
    await message.answer(
        text="Название вашего военного комиссариата изменено.",
    )
    await manager.switch_to(
        state=MyDataState.start,
    )

async def set_military_station_address(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager
) -> None:
    text = message.text
    manager.start_data["military_station_address"] = text
    manager.start_data["is_save"] = True
    await message.answer(
        text="Почтовый адрес и индекс военного комиссариата изменены."
    )
    await manager.switch_to(
        state=MyDataState.start,
    )


async def set_university(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    text = message.text
    manager.start_data["university"] = text
    manager.start_data["is_save"] = True
    await message.answer(
        text="Название вашего вуза изменено.",
    )
    await manager.switch_to(
        state=MyDataState.start,
    )


async def set_average_score(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    text = message.text
    try:
        score = float(text.replace(",", "."))
    except ValueError:
        await manager.switch_to(
            state=MyDataState.invalid_average_score,
        )
        return
    if score < 4:
        await manager.switch_to(
            state=MyDataState.low_average_score,
        )
        return
    elif score > 5:
        await manager.switch_to(
            state=MyDataState.invalid_average_score,
        )
        return
    manager.start_data["average_score"] = score
    manager.start_data["is_save"] = True
    await message.answer(
        text="Ваш средний балл изменен.",
    )
    await manager.switch_to(
        state=MyDataState.start,
    )


async def set_direction_training(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    text = message.text
    manager.start_data["direction_training"] = text
    manager.start_data["is_save"] = True
    await message.answer(
        text="Ваше направление подготовки изменено.",
    )
    await manager.switch_to(
        state=MyDataState.start,
    )


async def set_phone_number(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    try:
        text = message.contact.phone_number
        manager.start_data["phone_number"] = text
        manager.start_data["is_save"] = True
        keyboard = StartCandidateKeyboardButton(
            resize_keyboard=True,
            one_time_keyboard=True,
            is_persistent=True,
        )
        await message.answer(
            text="Ваш номер телефона изменен.",
            reply_markup=keyboard() if not manager.start_data.get(
                "is_registration",
            ) else None,
        )
        await manager.switch_to(
            state=MyDataState.start,
        )
    except AttributeError:
        await manager.switch_to(
            state=MyDataState.invalid_phone_number,
        )
        return
    except UnboundLocalError:
        await manager.switch_to(
            state=MyDataState.invalid_phone_number,
        )
        return


async def set_find_out(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    text = message.text
    manager.start_data["find_out"] = text
    manager.start_data["is_save"] = True
    manager.show_mode = ShowMode.SEND
    await manager.switch_to(
        state=MyDataState.start,
    )
