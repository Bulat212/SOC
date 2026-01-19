from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Button, Row

from bot.presentation.on_click.delete_candidate import cancel_delete_click, confirm_delete
from bot.presentation.state.delete_candidate import DeleteCandidateState

dialog = Dialog(
    Window(
        Const(
            "⚠️ Вы уверены, что хотите удалить свою кандидатуру?\n\n"
            "Это действие нельзя отменить."
        ),
        Row(
            Button(
                Const("❌ Отмена"),
                id="cancel_delete",
                on_click=cancel_delete_click,
            ),
            Button(
                Const("🗑️ Да, удалить"),
                id="confirm_delete",
                on_click=confirm_delete,
            ),
        ),
        state=DeleteCandidateState.confirm,
    ),
)
