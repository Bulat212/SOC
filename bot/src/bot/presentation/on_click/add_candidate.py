import asyncio
import datetime

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.kbd import Button

from bot.application.dto.candidate import AddCandidateDTO
from bot.application.usecase.candidate import CandidateUseCase
from bot.presentation.state.add_candidate import AddCandidateState
from bot.constants import FORMAT_BIRTHDATE, MIN_AGE, MAX_AGE

from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from bot.presentation.button.start_button import StartDelegateKeyboardButton
from bot.presentation.state.my_data import MyDataState

async def start_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=AddCandidateState.nationality,
    )


async def recruitment_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    data = dialog_manager.start_data
    recruitments = data.get("recruitments")
    item_id: str = dialog_manager.item_id  # noqa
    recruitment = recruitments[int(item_id) - 1]
    data["recruitment"] = recruitment
    await dialog_manager.switch_to(
        state=AddCandidateState.check_data,
        show_mode=ShowMode.EDIT,
    )


async def nationality_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    data = dialog_manager.start_data
    data["nationality"] = "РФ"
    await dialog_manager.switch_to(
        state=AddCandidateState.tertiary_education,
    )


async def invalid_nationality_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=AddCandidateState.invalid_nationality,
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
        state=AddCandidateState.invalid_tertiary_education,
    )


async def tertiary_education_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:

    await dialog_manager.switch_to(
        state=AddCandidateState.birthdate,
        show_mode=ShowMode.EDIT,
    )


@inject
async def right_click(
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
    keyboard = StartDelegateKeyboardButton(
        resize_keyboard=True,
        one_time_keyboard=True,
        is_persistent=True,
    )
    await cq.message.answer(
        text="Заявка кандидата успешно добавлена в базу! ",
        reply_markup=keyboard(),
    )
    await dialog_manager.reset_stack()



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
