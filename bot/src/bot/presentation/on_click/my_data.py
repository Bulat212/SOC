import datetime

from aiogram.types import CallbackQuery, MenuButtonWebApp, WebAppInfo
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, ManagedCalendar
from bot.config import BotConfig
from bot.presentation.utils.candidate import create_yandex_form_url, format_new_candidate_message
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.application.dto.candidate import UpdateCandidateDTO
from bot.application.usecase.candidate import CandidateUseCase
from bot.constants import FORMAT_BIRTHDATE, MIN_AGE, MAX_AGE
from bot.presentation.button.start_button import StartCandidateKeyboardButton
from bot.presentation.state.my_data import MyDataState


async def set_recruitment_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    data = dialog_manager.start_data
    recruitments = data.get("recruitments")
    item_id: str = dialog_manager.item_id  # noqa
    recruitment = recruitments[int(item_id)]
    data["recruitment"] = recruitment
    await dialog_manager.update(data)
    data["is_save"] = True
    await cq.message.answer(
        text="Ваша заявка на призыв изменена.",
    )
    await dialog_manager.switch_to(
        state=MyDataState.start,
    )


async def my_data_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=MyDataState.start,
    )


async def recruitment_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=MyDataState.recruitment,
    )


async def first_name_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=MyDataState.first_name,
    )


async def patronymic_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=MyDataState.patronymic,
    )


async def last_name_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=MyDataState.last_name,
    )


async def birthdate_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=MyDataState.birthdate,
    )


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
            state=MyDataState.invalid_period_birthdate,
        )
        return
    manager.start_data["birthdate"] = birthdate.strftime("%d.%m.%Y")
    manager.start_data["is_save"] = True
    await callback.message.answer(
        text="Ваша дата рождения изменена.",
    )
    await manager.switch_to(
        state=MyDataState.start,
    )


async def subject_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=MyDataState.subject,
    )


async def nationality_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=MyDataState.nationality,
    )


async def military_station_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=MyDataState.military_station,
    )


async def military_station_address_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=MyDataState.military_station_address,
    )


async def guarding_data_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=MyDataState.graduation_date,
    )


async def university_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=MyDataState.university,
    )


async def average_score_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=MyDataState.average_score,
    )


async def direction_training_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=MyDataState.direction_training,
    )


async def phone_number_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=MyDataState.phone_number,
    )


async def find_out_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=MyDataState.find_out,
    )


@inject
async def save_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
        usecase: FromDishka[CandidateUseCase],
        config: FromDishka[BotConfig],
) -> None:
    data = dialog_manager.start_data
    recruitment_id = None
    if data.get("recruitment") and isinstance(data.get("recruitment"), dict):
        recruitment_id = data.get("recruitment").get("id")
    request = UpdateCandidateDTO(
        telegram_id=data.get("telegram_id"),
        recruitment_id=recruitment_id,
        nationality=data.get("nationality"),
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        patronymic=data.get("patronymic"),
        birthdate=data.get("birthdate"),
        military_station=data.get("military_station"),
        military_station_address=data.get("military_station_address"),
        university=data.get("university"),
        direction_training=data.get("direction_training"),
        average_score=data.get("average_score"),
        find_out=data.get("find_out"),
        phone_number=data.get("phone_number"),
        subject=data.get("subject"),
        graduation_date=data.get("graduation_date"),
    )
    update_candidate = await usecase.update_candidate(request)
    if data.get("is_registration"):
        keyboard = StartCandidateKeyboardButton(
            resize_keyboard=True,
            one_time_keyboard=True,
            is_persistent=True,
        )

        username = data.get("username")

        url = create_yandex_form_url(update_candidate, username)

        await cq.bot.set_chat_menu_button(
            chat_id=cq.message.chat.id,
            menu_button=MenuButtonWebApp(
                text="Open",
                web_app=WebAppInfo(url=url)
            )
        )
        
        text = format_new_candidate_message(data)
        await cq.bot.send_message(
                chat_id=config.group_id,
                text=text,
                message_thread_id=config.new_registration_topic_id,
                parse_mode="HTML",
            )
        
        await cq.message.answer(
            text="Поздравляем, Ваша заявка принята. Ваша кандидатура "
                 "будет рассмотрена для поступления в научную роту "
                 "Военной академии связи им С.М. Буденного",
            reply_markup=keyboard(),
        )


        request.birthdate=datetime.datetime.strptime(
            data.get("birthdate"),
            FORMAT_BIRTHDATE,
        )
        request.graduation_date=datetime.datetime.strptime(
            data.get("graduation_date"),
            FORMAT_BIRTHDATE,
        )
        
        await usecase.new_registration_soc(request)

        await dialog_manager.reset_stack()
        return
    
    
    await cq.message.answer(
        text="Ваши данные изменены",
    )
    await dialog_manager.reset_stack()


async def set_nationality_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    data = dialog_manager.start_data
    data["nationality"] = "РФ"
    await cq.message.answer(
        text="Ваше гражданство изменено.",
    )
    await dialog_manager.switch_to(
        state=MyDataState.start,
    )


async def invalid_nationality_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=MyDataState.invalid_nationality,
    )


async def set_edit_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    dialog_manager.start_data["is_edit"] = True
    await dialog_manager.switch_to(
        state=MyDataState.start,
    )
