from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.kbd import Url
from aiogram_dialog.widgets.text import Const, Format, Case

from bot.presentation.getter.about_us import get_about_us
from bot.presentation.state.about_us import AboutUsState


def check_error(
        data: dict,
        widget: Whenable,
        manager: DialogManager,
) -> bool:
    error = data.get("error")
    if error is not None:
        return False
    return True


dialog = Dialog(
    Window(
        Case(
            {
                True: Const(
                    text="Для того, чтобы узнать о нас больше, переходите по ссылке "
                         "на рубрику в нашем телеграмм-канале.",
                ),
                False: Const(
                    text="<b>Скоро появится ссылка на наш телеграмм-канал.</b>",
                ),
            },
            selector="is_url",
        ),
        Url(
            text=Const(
                text="Узнать #О_нас",
            ),
            url=Format(
                text="{url}",
            ),
            when=check_error,
        ),
        state=AboutUsState.about_us_url,
        getter=get_about_us,
    ),
)
