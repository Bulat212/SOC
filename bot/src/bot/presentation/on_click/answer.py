from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from bot.presentation.button.start_button import StartDirectorKeyboardButton


async def cancel_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.done()
    user_id = cq.from_user.id
    keyboard = StartDirectorKeyboardButton(
        resize_keyboard=True,
        one_time_keyboard=True,
        is_persistent=True,
    )
    await cq.bot.send_message(
        chat_id=user_id,
        text="Отправка ответа отменена.",
        reply_markup=keyboard(),
    )
