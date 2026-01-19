from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Row, Button, ListGroup
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory
from aiogram_dialog.widgets.text import Const, Format, Case

from bot.presentation.func.question import set_question
from bot.presentation.getter.answer import get_answer
from bot.presentation.getter.question import (
    get_user_question, get_questions, get_question,
)
from bot.presentation.on_click.question import (
    off_answer_click,
    answer_click,
    cancel_click, question_back, question_next, question_click,
)
from bot.presentation.state.question import QuestionState


def check_question(
        data: dict,
        widget: Whenable,
        manager: DialogManager,
) -> bool:
    return data.get("is_question", False)


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
            text="Отправьте интересующий Вас вопрос",
        ),
        MessageInput(
            func=set_question,
            content_types=ContentType.TEXT,
        ),
        Button(
            text=Const(
                text="✖️ Отмена",
            ),
            id="cancel_btn",
            on_click=cancel_click,
        ),
        state=QuestionState.start,
        markup_factory=ReplyKeyboardFactory(
            resize_keyboard=True,
            one_time_keyboard=True,
            is_persistent=True,
        ),
    ),
    Window(
        Format(
            text=(
                "Заявка №{number}\n"
                "Ваш вопрос \"{question}\" зарегистрирован и поступил "
                "в обработку!"
            ),
        ),
        state=QuestionState.question,
        getter=get_question,
    ),
    Window(
        Format(
            text="Пользователь {name} задал вопрос:\n <b>{question}</b>",
        ),
        Row(
            Button(
                text=Const(
                    text="Ответить",
                ),
                id="answer_btn",
                on_click=answer_click,
            ),
            Button(
                text=Const(
                    text="Отложить ответ",
                ),
                id="off_answer_btn",
                on_click=off_answer_click,
            ),
        ),
        state=QuestionState.ask_question_director,
        getter=get_user_question,
    ),
    Window(
        Format(
            text="Ответ на Ваш вопрос (<i>{question}</i>):\n\n"
                 "{answer}",
        ),
        state=QuestionState.getting_question,
        getter=get_answer,
    ),
    Window(
        Case(
            {
                True: Const(
                    text="<b>Пользователи задали вопросы:</b>",
                ),
                False: Const(
                    text="<b>Пользователи не задали вопросы</b>",
                ),
            },
            selector="is_question",
        ),
        ListGroup(
            Button(
                text=Format(
                    text="{item[question]}",
                ),
                id="question_btn",
                on_click=question_click,
            ),
            id="questions",
            item_id_getter=lambda item: item["idx"],
            items="questions",
            when=check_question,
        ),
        Row(
            Button(
                text=Const(
                    text="⬅️",
                ),
                id="back_btn",
                on_click=question_back,
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
                on_click=question_next,
                when=check_is_next,
            ),
            when=check_question,
        ),
        state=QuestionState.question_list,
        getter=get_questions,
    ),
)
