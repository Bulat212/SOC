from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.application.dto.faq import AddFaqIDDTO
from bot.application.usecase.faq import FaqUseCase
from bot.presentation.state.faq import FaqState


async def faq_back(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    data = dialog_manager.start_data
    data["offset"] = data.get("offset", 0) - 1
    await dialog_manager.switch_to(
        state=FaqState.faq,
    )


async def faq_next(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    data = dialog_manager.start_data
    data["offset"] = data.get("offset", 0) + 1
    await dialog_manager.switch_to(
        state=FaqState.faq,
    )


async def send_faq(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    data = dialog_manager.start_data
    faq_list = data.get("faq")
    item_id: str = dialog_manager.item_id  # noqa
    faq = faq_list[int(item_id)]
    attrs = ["answer", "question", "id"]
    for attr in attrs:
        data[attr] = faq.get(attr)
    await dialog_manager.switch_to(
        state=FaqState.answer,
    )


async def set_question_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=FaqState.adding_question,
    )


@inject
async def delete_faq(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
        usecase: FromDishka[FaqUseCase],
) -> None:
    data = dialog_manager.start_data
    faq_id = data.get("id")
    request = AddFaqIDDTO(
        id=faq_id,
    )
    await usecase.delete(request)
    await dialog_manager.switch_to(
        state=FaqState.deleted_faq,
    )
