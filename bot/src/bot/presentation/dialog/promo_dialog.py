from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, ListGroup, Group
from aiogram_dialog.widgets.text import Const, Format, Case

from bot.presentation.func.promo import set_promo_name, set_promo_document
from bot.presentation.getter.promo import (
    get_promo_documents_name,
    add_promo_document,
)
from bot.presentation.on_click.promo import (
    send_document,
    add_promo,
    send_promo,
    delete_promo,
    send_photo_promo
)
from bot.presentation.state.promo import PromoState


def check_is_director(
        data: dict,
        widget: Whenable,
        manager: DialogManager,
) -> bool:
    is_director = data.get("is_director")
    return is_director


def check_is_promo(
        data: dict,
        widget: Whenable,
        manager: DialogManager,
) -> bool:
    is_promo = data.get("is_promo")
    return is_promo


dialog = Dialog(
    Window(
        Case(
            {
                True: Const(
                    text="Выберите интересующие Вас промо материалы:",
                ),
                False: Const(
                    text="<b>Скоро будут добавлены промо-материалы.</b>",
                ),
            },
            selector="is_promo",
        ),
        Group(
            ListGroup(
                Button(
                    text=Format(
                        text="{item[name]}",
                    ),
                    id="promo_btn",
                    # on_click=send_document,
                    on_click=send_photo_promo,
                    
                ),
                id="promo",
                item_id_getter=lambda item: item["idx"],
                items="promo",
            ),
            width=2,
            when=check_is_promo,
        ),
        Button(
            text=Const(
                text="Добавить",
            ),
            id="add_promo_btn",
            when=check_is_director,
            on_click=add_promo,
        ),
        state=PromoState.start,
        getter=get_promo_documents_name,
    ),
    Window(
        Const(
            text="Документ скоро будет добавлен",
        ),
        state=PromoState.invalid,
    ),
    Window(
        Const(
            text="Введите название для промо-материала:",
        ),
        MessageInput(
            func=set_promo_name,
        ),
        state=PromoState.adding_name,
    ),
    Window(
        Const(
            text="Отправьте файл:",
        ),
        MessageInput(
            func=set_promo_document,
        ),
        state=PromoState.adding_file,
    ),
    Window(
        Const(
            text="Файл сохранен.",
        ),
        state=PromoState.save_file,
        getter=add_promo_document,
    ),
    Window(
        Const(
            text="Что Вы хотите сделать с промо-материалом?",
        ),
        Group(
            Button(
                text=Const(
                    text="Получить",
                ),
                id="get_promo_btn",
                on_click=send_promo,
            ),
            Button(
                text=Const(
                    text="Удалить",
                ),
                id="delete_promo_btn",
                on_click=delete_promo,
            ),
            width=2,
        ),
        state=PromoState.question,
    ),
    Window(
        Const(
            text="Файл удален.",
        ),
        state=PromoState.delete_file,
    ),
)
