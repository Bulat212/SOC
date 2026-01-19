from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Row, Button
from aiogram_dialog.widgets.text import Const

from bot.presentation.on_click.info import (
    back_click,
    faq_click,
    promo_click,
    about_us_click,
    telegram_channel_click,
    sample_documents_click,
    guarding_document_click,
)
from bot.presentation.state.info import InfoState

dialog = Dialog(
    Window(
        Const(
            text="Информация о научной роте",
        ),
        Row(
            Button(
                text=Const(
                    text="❓ FAQ",
                ),
                id="faq_btn",
                on_click=faq_click,
            ),
            Button(
                text=Const(
                    text="📣 Промо",
                ),
                id="promo_btn",
                on_click=promo_click,
            ),
        ),
        Row(
            Button(
                text=Const(
                    text="👥 #О_нас",
                ),
                id="about_us_btn",
                on_click=about_us_click,
            ),
            Button(
                text=Const(
                    text="✈️ Telegram-канал",
                ),
                id="telegram_channel_btn",
                on_click=telegram_channel_click,
            ),
        ),
        Button(
            text=Const(
                text="📑 Образцы документов кандидата",
            ),
            id="sample_document_btn",
            on_click=sample_documents_click,
        ),
        Button(
            text=Const(
                text="📋 Руководящие документы",
            ),
            id="guidance_document_btn",
            on_click=guarding_document_click,
        ),
        Button(
            text=Const(
                text="Назад",
            ),
            id="back",
            on_click=back_click,
        ),
        state=InfoState.start,
    ),
)
