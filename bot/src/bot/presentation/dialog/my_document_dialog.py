from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Case

from bot.presentation.func.my_document import (
    set_form,
    set_approval,
    set_statement,
)
from bot.presentation.getter.my_document import (
    check_documents,
    get_is_form_sheet,
    get_is_approval,
    get_is_statement,
)
from bot.presentation.on_click.my_document import (
    form_click,
    approval_click,
    statement_click,
    cancel_click,
    send_form,
    send_approval,
    send_statement,
)
from bot.presentation.state.my_form import MyDocumentState

dialog = Dialog(
    Window(
        Const(
            text="Мои документы",
        ),
        Row(
            Button(
                text=Case(
                    {
                        True: Const(
                            text="✅ Лист собеседования",
                        ),
                        False: Const(
                            text="❌ Лист собеседования",
                        ),
                    },
                    selector="is_form",
                ),
                id="is_form_btn",
                on_click=form_click,
            ),
            Button(
                text=Case(
                    {
                        True: Const(
                            text="✅ Согласие на ОПД",
                        ),
                        False: Const(
                            text="❌ Согласие на ОПД",
                        ),
                    },
                    selector="is_approval",
                ),
                id="approval_btn",
                on_click=approval_click,
            ),
        ),
        Button(
            text=Case(
                {
                    True: Const(
                        text="✅ Заявление",
                    ),
                    False: Const(
                        text="❌ Заявление",
                    ),
                },
                selector="is_statement",
            ),
            id="statement_btn",
            on_click=statement_click,
        ),
        state=MyDocumentState.document,
        getter=check_documents,
    ),
    Window(
        Case(
            {
                True: Const(
                    text="Обновить лист собеседования?",
                ),
                False: Const(
                    text="Добавить лист собеседования?",
                ),
            },
            selector="is_form",
        ),
        Row(
            Button(
                text=Const(
                    text="Да",
                ),
                id="yes_btn",
                on_click=send_form,
            ),
            Button(
                text=Const(
                    text="Нет",
                ),
                id="no_btn",
                on_click=cancel_click,
            ),
        ),
        state=MyDocumentState.form,
        getter=get_is_form_sheet,
    ),
    Window(
        Const(
            text="Отправьте файл:",
        ),
        MessageInput(
            func=set_form,
        ),
        Button(
            text=Const(
                text="✖️ Отмена",
            ),
            id="cancel_btn",
            on_click=cancel_click,
        ),
        state=MyDocumentState.document_form,
    ),
    Window(
        Case(
            {
                True: Const(
                    text="Обновить согласие на обработку персональных данных?",
                ),
                False: Const(
                    text="Добавить согласие на обработку персональных данных?",
                ),
            },
            selector="is_approval",
        ),
        Row(
            Button(
                text=Const(
                    text="Да",
                ),
                id="yes_btn",
                on_click=send_approval,
            ),
            Button(
                text=Const(
                    text="Нет",
                ),
                id="no_btn",
                on_click=cancel_click,
            ),
        ),
        state=MyDocumentState.approval,
        getter=get_is_approval,
    ),
    Window(
        Const(
            text="Отправьте файл:",
        ),
        MessageInput(
            func=set_approval,
        ),
        Button(
            text=Const(
                text="✖️ Отмена",
            ),
            id="cancel_btn",
            on_click=cancel_click,
        ),
        state=MyDocumentState.document_approval,
    ),
    Window(
        Case(
            {
                True: Const(
                    text="Обновить заявление?",
                ),
                False: Const(
                    text="Добавить заявление?",
                ),
            },
            selector="is_statement",
        ),
        Row(
            Button(
                text=Const(
                    text="Да",
                ),
                id="yes_btn",
                on_click=send_statement,
            ),
            Button(
                text=Const(
                    text="Нет",
                ),
                id="no_btn",
                on_click=cancel_click,
            ),
        ),
        state=MyDocumentState.statement,
        getter=get_is_statement,
    ),
    Window(
        Const(
            text="Отправьте файл:",
        ),
        MessageInput(
            func=set_statement,
        ),
        Button(
            text=Const(
                text="✖️ Отмена",
            ),
            id="cancel_btn",
            on_click=cancel_click,
        ),
        state=MyDocumentState.document_statement,
    ),
)
