from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format, Case, Const

from bot.presentation.getter.telegram import get_telegram_channel_url
from bot.presentation.state.telegram import TelegramChannelState

dialog = Dialog(
    Window(
        Case(
            {
                True: Format(
                    text="{url}",
                ),
                False: Const(
                    text="<b>Ссылка на телеграмм-канал скоро добавится.</b>",
                ),
            },
            selector="is_url",
        ),
        state=TelegramChannelState.telegram_channel_url,
        getter=get_telegram_channel_url,
    ),
)
