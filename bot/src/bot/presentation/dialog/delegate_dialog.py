from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.input import MessageInput

from bot.presentation.state.delegate import RegistrationDelegateState

from bot.presentation.on_click.delegate import (
    start_click,
    skip_end_work_date,
    skip_start_work_date,
    skip_subject,
    start_delegate,
)

from bot.presentation.func.delegate import (
    set_end_work_date,
    set_last_name,
    set_first_name, 
    set_patronymic, 
    set_post,
    set_start_work_date, 
    set_subject,
)


dialog = Dialog(
    Window(
        Const(
            text="Для получения доступа к функционалу ответьте на несколько вопросов "
        ),
        Button(
            text=Const(
                text="Далее",
            ),
            id="next_btn",
            on_click=start_click,
        ),
        state=RegistrationDelegateState.start,

    ),
    Window(
        Const(
            text="Напишите Вашу Фамилию.",
        ),
        MessageInput(
            func=set_last_name
        ),
        state=RegistrationDelegateState.last_name,
    ),
    Window(
        Const(
            text="Напишите Ваше Имя.",
        ),
        MessageInput(
            func=set_first_name
        ),
        state=RegistrationDelegateState.first_name,
    ),
    Window(
        Const(
            text="Напишите Ваше Отчество.",
        ),
        MessageInput(
            func=set_patronymic
        ),
        state=RegistrationDelegateState.patronymic,
    ),
    Window(
        Const(
            text="Напишите Вашу Должность.",
        ),
        MessageInput(
            func=set_post
        ),
        state=RegistrationDelegateState.post,
    ),
    Window(
        Const(
            text="Напишите субъект агитации.",
        ),
        MessageInput(
            func=set_subject
        ),
        Button(
            text=Const(
                text="Пропустить",
            ),
            id="skip_subject",
            on_click=skip_subject,
        ),
        state=RegistrationDelegateState.subject,
    ),
    Window(
        Const(
            text="Укажите дату начала работ в формате дд.мм.гггг: "
        ),
        MessageInput(
            func=set_start_work_date
        ),
        Button(
            text=Const(
                text="Пропустить",
            ),
            id="skip_start_work_date",
            on_click=skip_start_work_date,
        ),
        state=RegistrationDelegateState.start_date,
    ),
    Window(
        Const(
            text="Введена некорректная дата, попробуйте снова.",
        ),
        MessageInput(
            func=set_start_work_date,
        ),
        state=RegistrationDelegateState.invalid_start_date,
    ),
    Window(
        Const(
            text="Укажите дату конца работ в формате дд.мм.гггг",
        ),
        MessageInput(
            func=set_end_work_date,
        ),
        Button(
            text=Const(
                text="Пропустить",
            ),
            id="skip_end_work_date",
            on_click=skip_end_work_date,
        ),
        state=RegistrationDelegateState.end_date,
    ),
    Window(
        Const(
            text="Введена некорректная дата, попробуйте снова.",
        ),
        MessageInput(
            func=set_end_work_date,
        ),
        state=RegistrationDelegateState.invalid_end_date,
    ),
    Window(
        Const(
            text="Поздравляю! Вам теперь открыт функционал чат-бота для работы с кандидатами."
        ),
        Button(
            text=Const(
                text="Приступить к работе",
            ),
            id="start_work",
            on_click=start_delegate,
        ),
        state=RegistrationDelegateState.finish,
    ),
)
