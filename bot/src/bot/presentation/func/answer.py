import asyncio

from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.application.dto.answer import AddAnswerDTO
from bot.application.usecase.answer import AnswerUseCase
from bot.presentation.button.start_button import StartDirectorKeyboardButton
from bot.presentation.state.question import QuestionState


@inject
async def set_answer(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
        usecase: FromDishka[AnswerUseCase],
) -> None:
    text = message.text
    manager.start_data["answer"] = text
    request = AddAnswerDTO(
        answer=text,
        question_id=manager.start_data.get("question_id"),
    )
    data = manager.start_data.copy()
    await usecase.add(request)
    await manager.reset_stack()
    keyboard = StartDirectorKeyboardButton(
        resize_keyboard=True,
        one_time_keyboard=True,
        is_persistent=True,
    )
    await message.answer(
        text="Ответ на вопрос сохранен.",
        reply_markup=keyboard(),
    )
    dialog_manager = manager.bg(
        user_id=data.get("user_id"),
        chat_id=data.get("user_id"),
    )
    await dialog_manager.start(
        state=QuestionState.getting_question,
        data=data,
        mode=StartMode.NORMAL,
        show_mode=ShowMode.SEND,
    )
    asyncio.create_task(dialog_manager.done())
