from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Url, Button, Row
from aiogram_dialog.widgets.text import Const

from bot.presentation.on_click.document import send_document, send_image
from bot.presentation.state.document import (
    DocumentState,
)

dialog = Dialog(
    Window(
        Const(
            text="ФЗ № 53 «О воинской обязанности и военной службе» "
                 "от 28.03.1998 (ред. 02.10.2024)",
        ),
        Button(
            text=Const(
                "📋 Требования к кандидатам",
            ),
            id="requirement_btn",
            on_click=send_document,
        ),
        Button(
            text=Const(
                text="🎓 Перечень специальностей",
            ),
            id="profession_btn",
            on_click=send_document,
        ),
        state=DocumentState.start_guarding,
    ),
    Window(
        Const(
            text="Образцы документов:",
        ),
        Button(
            text=Const(
                text="📝 Лист собеседования",
            ),
            id="interview_sheet_btn",
            on_click=send_document,
        ),
        Row(
            Button(
                text=Const(
                    text="📄 Согласие",
                ),
                id="approval_btn",
                on_click=send_document,
            ),
            Button(
                text=Const(
                    text="📄 Заявление",
                ),
                id="statement_btn",
                on_click=send_image,
            ),
        ),
        state=DocumentState.start,
    ),
    Window(
        Const(
            text="<b>Документ скоро будет добавлен</b>",
        ),
        state=DocumentState.invalid,
    ),
)
