from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from bot.presentation.state.get_candidate import GetCandidateState


async def recruitment_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    data = dialog_manager.dialog_data
    recruitments = data.get("recruitments")
    item_id: str = dialog_manager.item_id  # noqa
    recruitment = recruitments[int(item_id)]
    
    dialog_manager.dialog_data["recruitment"] = recruitment
    await dialog_manager.switch_to(
        state=GetCandidateState.candidate_list,
    )


async def faq_back(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
    ) -> None:
    data = dialog_manager.start_data
    data["offset"] = data.get("offset", 0) - 1
    await dialog_manager.switch_to(
        state=GetCandidateState.candidate_list,
    )


async def faq_next(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    data = dialog_manager.start_data
    data["offset"] = data.get("offset", 0) + 1
    await dialog_manager.switch_to(
        state=GetCandidateState.candidate_list,
    )


async def next_page(callback, button, dialog_manager: DialogManager):
    dialog_manager.dialog_data["page"] += 1
    await dialog_manager.show()

async def prev_page(callback, button, dialog_manager: DialogManager):
    dialog_manager.dialog_data["page"] -= 1
    await dialog_manager.show()