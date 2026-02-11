from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.kbd import (
    Button,
    ListGroup,
    Group,
    Row,
)
from aiogram_dialog.widgets.text import Const, Format

from bot.presentation.getter.get_candidates import get_candidates_list
from bot.presentation.getter.get_candidates import get_recruitments
from bot.presentation.on_click.get_candidate import candidate_click, next_page, prev_page, recruitment_click
from bot.presentation.state.get_candidate import GetCandidateState


import logging
def check_is_pages(
        data: dict,
        widget: Whenable,
        manager: DialogManager,
) -> bool:
    pages = data.get("pages")
    if pages==0:
        return False
    return True

def check_candidates(
        data: dict,
        widget: Whenable,
        manager: DialogManager,
) -> bool:
    return data.get("is_candidate", False)


def check_is_back(
        data: dict,
        widget: Whenable,
        manager: DialogManager,
) -> bool:
    is_back = data.get("is_back")
    return is_back


def check_is_next(
        data: dict,
        widget: Whenable,
        manager: DialogManager,
) -> bool:
    is_next = data.get("is_next")
    return is_next


dialog = Dialog(
    Window(
        Const(
            text="Выберите время призыва:",
        ),
        Group(
            ListGroup(
                Button(
                    text=Format(
                        text="{item[name]}",
                    ),
                    id="recruitment_btn",
                    on_click=recruitment_click,
                ),
                id="recruitments",
                item_id_getter=lambda item: item["idx"],
                items="recruitments",
            ),
            width=2,
        ),
        state=GetCandidateState.recruitment,
        getter=get_recruitments,
    ),
    Window(
        Format("Кандидаты по призыву {recruitment_name}:"),
        Group(
            ListGroup(
                Button(
                    text=Format(
                        text="{item[first_name]}, Статус заявки:{item[is_approval]}",
                    ),
                    id="candidates_btn",
                    on_click=candidate_click,
                ),
                id="candidates",
                item_id_getter=lambda item: item["id"],
                items="candidates",
            ),
            when=check_candidates,
        ),
        Row(
            Button(Const("⬅️"), id="prev", on_click=prev_page, when=check_is_back),
            Button(Format("{page}/{pages}"), id="pages", when=check_is_pages),
            Button(Const("➡️"), id="next", on_click=next_page, when=check_is_next),
            when=check_candidates,
        ),
        state=GetCandidateState.candidate_list,
        getter=get_candidates_list,
    ),
    Window(
        Const(
            text="Форма кандидата:",
        ),
        state=GetCandidateState.candidate_form,
        # getter=get_candidates_list,
    ),
)