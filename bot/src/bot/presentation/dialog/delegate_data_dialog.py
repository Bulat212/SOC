from aiogram import F
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (
    Button,
    Row,
)
from aiogram_dialog.widgets.text import Format, Const

from bot.presentation.func.delegate_data import (
    set_first_name,
    set_patronymic,
    set_last_name,
    set_subject,
    set_post,
    set_end_work_date,
    set_start_work_date,
)
from bot.presentation.getter.delegate import get_delegate
from bot.presentation.on_click.delegate_data import (
    end_date_click,
    post_click,
    delegate_data_click,
    first_name_click,
    patronymic_click,
    last_name_click,
    start_date_click,
    save_click,
    subject_click,
    set_edit_click,
)
from bot.presentation.state.delegate_data import DelegateDataState


def check_is_save(
        data: dict[str, str],
        widget: Whenable,
        manager: DialogManager,
) -> bool:
    return data.get("is_save", False)


dialog = Dialog(
    Window(
        Format(
            text="Ваши данные:\n\n"
                 "<b>Фамилия:</b> <u>{last_name}</u>\n"
                 "<b>Имя:</b> <u>{first_name}</u>\n"
                 "<b>Отчество:</b> <u>{patronymic}</u>\n"
                 "<b>Должность:</b> <u>{post}</u>\n"
                 "<b>Субъект работы:</b> <u>{subject}</u>\n"
                 "<b>Дата начала работ:</b> <u>{start_date}</u>\n"
                 "<b>Дата конца работ:</b> <u>{end_date}</u>\n"
        ),
        Button(
            text=Const(
                text="✏️ Редактировать",
            ),
            id="edit_btn",
            on_click=set_edit_click,
            when=~F["is_edit"],
        ),
        Row(
            Button(
                text=Const(
                    text="Фамилия",
                ),
                id="last_name_btn",
                on_click=last_name_click,
            ),
            Button(
                text=Const(
                    text="Имя",
                ),
                id="first_name_btn",
                on_click=first_name_click,
            ),
            when=F["is_edit"],
        ),
        Button(
            text=Const(
                text="Отчество",
            ),
            id="patronymic_btn",
            on_click=patronymic_click,
            when=F["is_edit"],
        ),
        Row(
            Button(
                text=Const(
                    text="Должность",
                ),
                id="post_btn",
                on_click=post_click,
            ),
            when=F["is_edit"],
        ),
        Button(
            text=Const(
                text="Субъект работы",
            ),
            id="subject_btn",
            on_click=subject_click,
            when=F["is_edit"],
        ),
        Button(
            text=Const(
                text="Дата начала работ",
            ),
            id="start_work_btn",
            on_click=start_date_click,
            when=F["is_edit"],
        ),
        Row(
            Button(
                text=Const(
                    text="Дата конца работ",
                ),
                id="end_work_btn",
                on_click=end_date_click,
            ),
            when=F["is_edit"],
        ),
        Button(
            text=Const(
                text="Сохранить ✅",
            ),
            id="save_btn",
            on_click=save_click,
            when=check_is_save,
        ),
        state=DelegateDataState.start,
        getter=get_delegate,
    ),
    Window(
        Const(
            text="Напишите Ваше имя",
        ),
        MessageInput(
            func=set_first_name,
        ),
        Button(
            text=Const(
                text="Мои данные",
            ),
            id="delegate_date_btn",
            on_click=delegate_data_click,
        ),
        state=DelegateDataState.first_name,
    ),
    Window(
        Const(
            text="Напишите Ваше отчество.",
        ),
        MessageInput(
            func=set_patronymic,
        ),
        Button(
            text=Const(
                text="Мои данные",
            ),
            id="delegate_date_btn",
            on_click=delegate_data_click,
        ),
        state=DelegateDataState.patronymic,
    ),
    Window(
        Const(
            text="Напишите Вашу Фамилию.",
        ),
        MessageInput(
            func=set_last_name,
        ),
        Button(
            text=Const(
                text="Мои данные",
            ),
            id="delegate_date_btn",
            on_click=delegate_data_click,
        ),
        state=DelegateDataState.last_name,
    ),
    Window(
        Const(
            text="Укажите субъект в котором Вы работаете:",
        ),
        MessageInput(
            func=set_subject,
        ),
        state=DelegateDataState.subject,
    ),
    Window(
        Const(
            text="Укажите Вашу должность:",
        ),
        MessageInput(
            func=set_post,
        ),
        state=DelegateDataState.post,
    ),
    Window(
        Const(
            text="Укажите дату начала работ в формате дд.мм.гггг",
        ),
        MessageInput(
            func=set_start_work_date,
        ),
        Button(
            text=Const(
                text="Мои данные",
            ),
            id="delegate_date_btn",
            on_click=delegate_data_click,
        ),
        state=DelegateDataState.start_date,
    ),
    Window(
        Const(
            text="Введена некорректная дата, попробуйте снова.",
        ),
        MessageInput(
            func=set_start_work_date,
        ),
        Button(
            text=Const(
                text="Мои данные",
            ),
            id="delegate_date_btn",
            on_click=delegate_data_click,
        ),
        state=DelegateDataState.invalid_start_date,
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
                text="Мои данные",
            ),
            id="delegate_date_btn",
            on_click=delegate_data_click,
        ),
        state=DelegateDataState.end_date,
    ),
    Window(
        Const(
            text="Введена некорректная дата, попробуйте снова.",
        ),
        MessageInput(
            func=set_end_work_date,
        ),
        Button(
            text=Const(
                text="Мои данные",
            ),
            id="delegate_date_btn",
            on_click=delegate_data_click,
        ),
        state=DelegateDataState.invalid_end_date,
    ),
    Window(
        Const(
            text="Ваши данные изменены",
        ),
        state=DelegateDataState.save,
    ),
)
