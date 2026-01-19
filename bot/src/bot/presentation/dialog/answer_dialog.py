from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory
from aiogram_dialog.widgets.text import Const

from bot.presentation.func.answer import set_answer
from bot.presentation.on_click.answer import cancel_click
from bot.presentation.state.answer import AnswerState

dialog = Dialog(
    Window(
        Const(
            text="Введите Ваш ответ:",
        ),
        MessageInput(
            func=set_answer,
        ),
        Button(
            text=Const(
                text="✖️ Отмена",
            ),
            id="cancel_btn",
            on_click=cancel_click,
        ),
        state=AnswerState.start,
        markup_factory=ReplyKeyboardFactory(
            resize_keyboard=True,
            one_time_keyboard=True,
            is_persistent=True,
        ),
    ),
    Window(
        Const(
            text="На данный вопрос уже ответили.",
        ),
        state=AnswerState.invalid,
    ),
)
