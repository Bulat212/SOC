from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Case, Const

from bot.presentation.getter.status import get_status
from bot.presentation.state.status import StatusState

dialog = Dialog(
    Window(
        Case(
            {
                "REVIEWED": Const(
                    text="Ваша заявка в научную роту одобрена. \n"
                         "Скоро с Вами свяжется наш представитель.",
                ),
                "UNDER_REVIEW": Const(
                    text="Ваша заявка находится на рассмотрении администрации.",
                ),
                "REJECTED": Const(
                    text="Увы, Ваша заявка в научную роту отклонена. "
                         "Однако не расстраивайтесь, мы сохранили "
                         "Вашу анкету и Вы сможете поучаствовать в наборе "
                         "в научную роту в следующем призыве.",
                ),
            },
            selector="status",
        ),
        state=StatusState.status,
        getter=get_status,
    ),
)
