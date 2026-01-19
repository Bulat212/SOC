import asyncio

from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.widgets.input import MessageInput

from bot.constants import LIMIT_FAQ, ZERO
from bot.presentation.state.faq import FaqState


async def set_question(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    text = message.text
    data = manager.start_data
    data["question"] = text
    await manager.switch_to(
        state=FaqState.adding_answer,
    )


async def set_answer(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    text = message.text
    data = manager.start_data
    data["answer"] = text
    await manager.switch_to(
        state=FaqState.adding_faq,
        show_mode=ShowMode.SEND,
    )
    asyncio.create_task(
        manager.bg(
            user_id=message.from_user.id,
            chat_id=message.chat.id,
        ).start(
            state=FaqState.faq,
            show_mode=ShowMode.SEND,
            mode=StartMode.RESET_STACK,
            data={
                "limit": LIMIT_FAQ,
                "offset": ZERO,
                "role": data.get("role"),
            },
        ),
    )
