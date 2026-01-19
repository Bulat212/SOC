import datetime

from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput

from bot.constants import FORMAT_BIRTHDATE, MIN_AGE, MAX_AGE
from bot.presentation.state.registration import RegistrationCandidateState


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
            state=RegistrationCandidateState.direction_training,
        )
        return
    except ValueError:
        await manager.switch_to(
            state=RegistrationCandidateState.invalid_graduation_date,
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
            await message.answer(
                text="В Соответствии с положениями п.п.\"а\", пункта 1, "
                     "статьи 22 \"Граждане, подлежащие призыву на военную "
                     "службу\" Федерального закона от 28.03.1998 N 53-ФЗ "
                     "(ред. от 02.10.2024) \"О воинской обязанности и военной "
                     "службе\", призыву на военную службу подлежат граждане "
                     "мужского пола в возрасте от 18 до 30 лет, состоящие "
                     "на воинском учете или не состоящие, но обязанные состоять "
                     "на воинском учете и не пребывающие в запасе",
            )
            await manager.done()
            return
        manager.start_data["birthdate"] = text
        await manager.switch_to(
            state=RegistrationCandidateState.last_name,
        )
    except ValueError:
        await manager.switch_to(
            state=RegistrationCandidateState.invalid_birthdate,
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
        state=RegistrationCandidateState.military_station,
    )


async def set_last_name(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    text = message.text
    manager.start_data["last_name"] = text
    await manager.switch_to(
        state=RegistrationCandidateState.first_name,
    )


async def set_first_name(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    text = message.text
    manager.start_data["first_name"] = text
    await manager.switch_to(
        state=RegistrationCandidateState.patronymic,
    )


async def set_patronymic(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    text = message.text
    manager.start_data["patronymic"] = text
    await manager.switch_to(
        state=RegistrationCandidateState.subject,
    )


async def set_military_station(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    text = message.text
    manager.start_data["military_station"] = text
    await manager.switch_to(
        state=RegistrationCandidateState.military_station_address,
    )


async def set_military_station_address(
        message: Message,
        manage_input: MessageInput,
        manager: DialogManager,
) -> None:
    text = message.text
    manager.start_data["military_station_address"] = text
    await manager.switch_to(
        state=RegistrationCandidateState.university,
    )


async def set_university(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    text = message.text
    manager.start_data["university"] = text
    await manager.switch_to(
        state=RegistrationCandidateState.graduation_date,
    )


async def set_direction_training(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    text = message.text
    manager.start_data["direction_training"] = text
    await manager.switch_to(
        state=RegistrationCandidateState.average_score,
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
            state=RegistrationCandidateState.invalid_average_score,
        )
        return
    if score <= 4:
        await manager.switch_to(
            state=RegistrationCandidateState.low_average_score,
        )
        await message.answer(
            text="Ваш средний балл не соответствует требованиям. "
                "В научную роту рассматриваются кандидаты со средним "
                "баллом не менее 4.0.",
            )
        await manager.done()
        return
    elif score > 5:
        await manager.switch_to(
            state=RegistrationCandidateState.invalid_average_score,
        )
        return
    await manager.switch_to(
        state=RegistrationCandidateState.find_out,
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
        state=RegistrationCandidateState.phone_number,
        show_mode=ShowMode.SEND,
    )


async def set_phone_number(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    try:
        text = message.contact.phone_number
        manager.start_data["phone_number"] = text
        await manager.switch_to(
            state=RegistrationCandidateState.recruitment,
        )
    except AttributeError:
        await manager.switch_to(
            state=RegistrationCandidateState.invalid_phone_number,
        )
        return
    except UnboundLocalError:
        await manager.switch_to(
            state=RegistrationCandidateState.invalid_phone_number,
        )
        return
