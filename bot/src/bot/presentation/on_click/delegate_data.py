from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from bot.application.dto.delegate import UpdateDelegateDTO
from bot.application.usecase.delegate import DelegateUseCase
from bot.presentation.state.delegate_data import DelegateDataState
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject


async def first_name_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=DelegateDataState.first_name,
    )


async def patronymic_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=DelegateDataState.patronymic,
    )


async def last_name_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=DelegateDataState.last_name,
    )


async def subject_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=DelegateDataState.subject,
    )


async def post_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=DelegateDataState.post,
    )


async def start_date_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=DelegateDataState.start_date,
    )


async def end_date_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=DelegateDataState.end_date,
    )


@inject
async def save_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
        usecase: FromDishka[DelegateUseCase],
) -> None:
    data = dialog_manager.start_data
    request = UpdateDelegateDTO(
        telegram_id=data.get("telegram_id"),
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        patronymic=data.get("patronymic"),
        post=data.get("post"),
        subject=data.get("subject"),
        start_date=data.get("start_date"),
        end_date=data.get("end_date"),
    )

    await usecase.update_delegate(request)
    await cq.message.answer(
        text="Ваши данные изменены",
    )
    await dialog_manager.reset_stack()


async def set_edit_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    dialog_manager.start_data["is_edit"] = True
    await dialog_manager.switch_to(
        state=DelegateDataState.start,
    )


async def delegate_data_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=DelegateDataState.start,
    )
