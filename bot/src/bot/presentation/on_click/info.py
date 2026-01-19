from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button

from bot.constants import LIMIT_FAQ, ZERO
from bot.domain.exception.info import InfoNotFound
from bot.presentation.button.start_button import StartCandidateKeyboardButton, StartDelegateKeyboardButton
from bot.presentation.state.about_us import AboutUsState
from bot.presentation.state.document import DocumentState
from bot.presentation.state.faq import FaqState
from bot.presentation.state.promo import PromoState
from bot.presentation.state.telegram import TelegramChannelState


async def faq_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    data = dialog_manager.start_data
    await dialog_manager.done()
    await dialog_manager.start(
        state=FaqState.faq,
        mode=StartMode.NORMAL,
        data={
            "limit": LIMIT_FAQ,
            "offset": ZERO,
            "role": data.get("role"),
        },
    )


async def promo_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    data = dialog_manager.start_data
    await dialog_manager.done()
    await dialog_manager.start(
        state=PromoState.start,
        mode=StartMode.NORMAL,
        data=data,
    )


async def about_us_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.done()
    try:
        await dialog_manager.start(
            state=AboutUsState.about_us_url,
            mode=StartMode.NORMAL,
        )
    except InfoNotFound:
        return


async def telegram_channel_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.done()
    try:
        await dialog_manager.start(
            state=TelegramChannelState.telegram_channel_url,
            mode=StartMode.NORMAL,
        )
    except InfoNotFound:
        return


async def sample_documents_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.done()
    try:
        await dialog_manager.start(
            state=DocumentState.start,
            mode=StartMode.NORMAL,
        )
    except InfoNotFound:
        return


async def guarding_document_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.done()
    try:
        await dialog_manager.start(
            state=DocumentState.start_guarding,
            mode=StartMode.NORMAL,
        )
    except InfoNotFound:
        return


async def back_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    message = dialog_manager.event.message
    role = dialog_manager.start_data.get("role")
    await dialog_manager.done()
    if(role=="delegate"):
        keyboard = StartDelegateKeyboardButton(
                            resize_keyboard=True,
                            one_time_keyboard=True,
                            is_persistent=True,
                        )
    if(role=="candidate"):
        keyboard = StartCandidateKeyboardButton(
                            resize_keyboard=True,
                            one_time_keyboard=True,
                            is_persistent=True,
                        )
    
    await message.answer(
                text="Выберете интересующий Вас раздел 👇",
                reply_markup=keyboard(),
            )