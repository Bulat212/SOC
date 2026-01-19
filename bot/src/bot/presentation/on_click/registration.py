import asyncio
import datetime

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.widgets.kbd import Button, ManagedCalendar
from bot.application.dto.candidate import AddCandidateDTO
from bot.application.usecase.candidate import CandidateUseCase
from bot.constants import FORMAT_BIRTHDATE, MIN_AGE, MAX_AGE
from bot.presentation.button.start_button import StartCandidateKeyboardButton
from bot.presentation.state.my_data import MyDataState
from bot.presentation.state.registration import RegistrationCandidateState
from bot.config import BotConfig
from bot.presentation.utils.candidate import format_new_candidate_message
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject


async def start_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=RegistrationCandidateState.nationality,
    )


async def recruitment_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    data = dialog_manager.start_data
    recruitments = data.get("recruitments")
    item_id: str = dialog_manager.item_id  # noqa
    recruitment = recruitments[int(item_id)]
    data["recruitment"] = recruitment
    await dialog_manager.switch_to(
        state=RegistrationCandidateState.check_data,
    )


async def nationality_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    data = dialog_manager.start_data
    data["nationality"] = "РФ"
    await dialog_manager.switch_to(
        state=RegistrationCandidateState.tertiary_education,
    )


async def invalid_nationality_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=RegistrationCandidateState.invalid_nationality,
    )
    asyncio.create_task(
        dialog_manager.reset_stack(),
    )


async def invalid_tertiary_education_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=RegistrationCandidateState.invalid_tertiary_education,
    )
    asyncio.create_task(
        dialog_manager.reset_stack(),
    )


async def tertiary_education_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=RegistrationCandidateState.birthdate,
        show_mode=ShowMode.EDIT,
    )


@inject
async def right_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
        usecase: FromDishka[CandidateUseCase],
        config: FromDishka[BotConfig],
) -> None:
    data = dialog_manager.start_data
    request = AddCandidateDTO(
        telegram_id=str(data.get("user_id")),
        recruitment_id=data.get("recruitment").get("id"),
        nationality=data.get("nationality"),
        username=data.get("username"),
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        patronymic=data.get("patronymic"),
        birthdate=datetime.datetime.strptime(
            data.get("birthdate"),
            FORMAT_BIRTHDATE,
        ),
        military_station=data.get("military_station"),
        military_station_address=data.get("military_station_address"),
        university=data.get("university"),
        average_score=data.get("average_score"),
        find_out=data.get("find_out"),
        phone_number=data.get("phone_number"),
        direction_training=data.get("direction_training"),
        subject=data.get("subject"),
        graduation_date=datetime.datetime.strptime(
            data.get("graduation_date"),
            FORMAT_BIRTHDATE,
        ),
    )
    await usecase.add_candidate(request)
    keyboard = StartCandidateKeyboardButton(
        resize_keyboard=True,
        one_time_keyboard=True,
        is_persistent=True,
    )
    await cq.message.answer(
        text="Поздравляем, Ваша заявка принята! Ваша кандидатура "
             "будет рассмотрена для поступления в научную роту "
             "Военной академии связи им С.М. Буденного!",
        reply_markup=keyboard(),
    )

    text = format_new_candidate_message(data)
    bot = cq.bot
    await bot.send_message(
                chat_id=config.group_id,
                text=text,
                message_thread_id=config.new_registration_topic_id,
                parse_mode="HTML",
            )

    await dialog_manager.reset_stack()


async def set_birthdate_click(
        callback: CallbackQuery,
        widget: ManagedCalendar,
        manager: DialogManager,
        selected_date: datetime.date,
) -> None:
    birthdate = selected_date
    today = datetime.date.today()
    age = today.year - birthdate.year - (
            (today.month, today.day) < (birthdate.month, birthdate.day)
    )
    if MIN_AGE > age or MAX_AGE < age:
        await manager.switch_to(
            state=RegistrationCandidateState.invalid_period_birthdate,
        )
        asyncio.create_task(manager.reset_stack())
        return
    manager.start_data["birthdate"] = birthdate.strftime("%d.%m.%Y")
    await manager.switch_to(
        state=RegistrationCandidateState.subject,
    )


async def set_graduation_date(
        callback: CallbackQuery,
        widget: ManagedCalendar,
        manager: DialogManager,
        selected_date: datetime.date,
) -> None:
    manager.start_data["graduation_date"] = selected_date.strftime("%d.%m.%Y")
    await manager.switch_to(
        state=RegistrationCandidateState.direction_training,
    )


@inject
async def incorrect_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
        usecase: FromDishka[CandidateUseCase],
) -> None:
    data = dialog_manager.start_data
    request = AddCandidateDTO(
        telegram_id=str(data.get("user_id")),
        recruitment_id=data.get("recruitment").get("id"),
        nationality=data.get("nationality"),
        username=data.get("username"),
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        patronymic=data.get("patronymic"),
        birthdate=datetime.datetime.strptime(
            data.get("birthdate"),
            FORMAT_BIRTHDATE,
        ),
        military_station=data.get("military_station"),
        military_station_address=data.get("military_station_address"),
        university=data.get("university"),
        average_score=data.get("average_score"),
        find_out=data.get("find_out"),
        phone_number=data.get("phone_number"),
        direction_training=data.get("direction_training"),
        subject=data.get("subject"),
        graduation_date=datetime.datetime.strptime(
            data.get("graduation_date"),
            FORMAT_BIRTHDATE,
        ),
    )
    await usecase.add_candidate(request)
    dialog_manager.start_data["is_registration"] = True
    dialog_manager.start_data["is_save"] = True
    data = dialog_manager.start_data.copy()
    data["telegram_id"] = str(data.get("user_id"))
    user_id = cq.from_user.id
    await dialog_manager.bg(
        user_id=user_id,
        chat_id=user_id,
    ).start(
        state=MyDataState.start,
        mode=StartMode.NORMAL,
        data=data,
    )
