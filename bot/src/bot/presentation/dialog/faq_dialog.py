from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import ListGroup, Button, Row
from aiogram_dialog.widgets.text import Const, Case, Format

from bot.presentation.func.faq import set_question, set_answer
from bot.presentation.getter.faq import get_faq_list, get_answer, add_faq
from bot.presentation.on_click.faq import (
    faq_back,
    faq_next,
    send_faq,
    set_question_click,
    delete_faq,
)
from bot.presentation.state.faq import FaqState


def check_faq(
        data: dict,
        widget: Whenable,
        manager: DialogManager,
) -> bool:
    return data.get("is_faq", False)


def check_is_back(
        data: dict,
        widget: Whenable,
        manager: DialogManager,
) -> bool:
    is_back = data.get("is_back")
    return is_back


def check_is_director(
        data: dict,
        widget: Whenable,
        manager: DialogManager,
) -> bool:
    is_director = data.get("is_director")
    return is_director


def check_is_next(
        data: dict,
        widget: Whenable,
        manager: DialogManager,
) -> bool:
    is_next = data.get("is_next")
    return is_next


dialog = Dialog(
    Window(
        Case(
            {
                True: Const(
                    text="<b>Выберите интересующий вас вопрос:</b>",
                ),
                False: Const(
                    text="<b>Скоро будут опубликованы "
                         "часто задаваемые вопросы</b>",
                ),
            },
            selector="is_faq",
        ),
        ListGroup(
            Button(
                text=Format(
                    text="{item[question]}",
                ),
                id="question_btn",
                on_click=send_faq,
            ),
            id="faq",
            item_id_getter=lambda item: item["idx"],
            items="faq",
            when=check_faq,
        ),
        Row(
            Button(
                text=Const(
                    text="⬅️",
                ),
                id="back_btn",
                on_click=faq_back,
                when=check_is_back,
            ),
            Button(
                text=Format(
                    text="{page}/{pages}",
                ),
                id="number_btn",
            ),
            Button(
                text=Const(
                    text="➡️",
                ),
                id="next_btn",
                on_click=faq_next,
                when=check_is_next,
            ),
            when=check_faq,
        ),
        Button(
            text=Const(
                text="Добавить FAQ",
            ),
            id="add_faq_btn",
            when=check_is_director,
            on_click=set_question_click,
        ),
        state=FaqState.faq,
        getter=get_faq_list,
    ),
    Window(
        Format(
            text="<b>{question}</b>\n\n\"<i>{answer}</i>\"",
        ),
        Button(
            text=Const(
                text="Удалить",
            ),
            id="delete_btn",
            on_click=delete_faq,
            when=check_is_director,
        ),
        state=FaqState.answer,
        getter=get_answer,
    ),
    Window(
        Const(
            text="Добавьте Ваш вопрос:",
        ),
        MessageInput(
            func=set_question,
        ),
        state=FaqState.adding_question,
    ),
    Window(
        Const(
            text="Добавьте Ваш ответ:",
        ),
        MessageInput(
            func=set_answer,
        ),
        state=FaqState.adding_answer,
    ),
    Window(
        Const(
            text="Вопрос с ответом добавлен в базу данных.",
        ),
        state=FaqState.adding_faq,
        getter=add_faq,
    ),
    Window(
        Const(
            text="Вопрос с ответом удален с базы данных.",
        ),
        state=FaqState.deleted_faq,
    ),
)
