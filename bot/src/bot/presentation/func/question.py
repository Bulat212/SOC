import asyncio

from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.application.usecase.user import UserUseCase
from bot.config import BotConfig
from bot.presentation.button.start_button import StartCandidateKeyboardButton
from bot.presentation.state.question import QuestionState
from bot.presentation.utils.user import get_username_or_full_name


@inject
async def set_question(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
        usecase: FromDishka[UserUseCase],
) -> None:
    text = message.text
    manager.start_data["question"] = text
    username = get_username_or_full_name(message=message)
    manager.start_data["username"] = username
    keyboard = StartCandidateKeyboardButton(
        resize_keyboard=True,
        one_time_keyboard=True,
        is_persistent=True,
    )
    data = manager.start_data.copy()
    await manager.done()
    await manager.start(
        state=QuestionState.question,
        mode=StartMode.NORMAL,
        data=data,
    )
    await asyncio.sleep(1)
    asyncio.create_task(manager.reset_stack())
    await message.answer(
        text="В ближайшее время администрация ответит на него и Вам придет "
             "уведомление!",
        reply_markup=keyboard(),
    )
    user_id_list = await usecase.get_director_id_all()
    for val in user_id_list.values:
        try:
            await manager.bg(
                user_id=int(val.telegram_id),
                chat_id=int(val.telegram_id),
            ).start(
                state=QuestionState.ask_question_director,
                mode=StartMode.NORMAL,
                data={
                    "question_id": data.get("question_id"),
                    "user_id": data.get("user_id"),
                    "question": data.get("question"),
                    "username": data.get("username"),
                },
                show_mode=ShowMode.SEND,
            )
        except TelegramForbiddenError:
            pass
