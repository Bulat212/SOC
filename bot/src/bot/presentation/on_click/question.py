from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.application.dto.question import AddQuestionIDDTO
from bot.application.dto.user import UserIDDTO
from bot.application.usecase.question import QuestionUseCase
from bot.application.usecase.user import UserUseCase
from bot.presentation.button.start_button import StartCandidateKeyboardButton
from bot.presentation.state.answer import AnswerState
from bot.presentation.state.question import QuestionState


async def off_answer_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.done()


@inject
async def answer_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
        usecase: FromDishka[QuestionUseCase],
) -> None:
    data = dialog_manager.start_data
    question_id = data.get("question_id")
    request = AddQuestionIDDTO(
        question_id=question_id,
    )
    question = await usecase.get(request)
    if question.is_answer:
        await dialog_manager.start(
            state=AnswerState.invalid,
            mode=StartMode.NORMAL,
        )
        return
    data["user_id"] = question.user_id
    await dialog_manager.done()
    await dialog_manager.start(
        state=AnswerState.start,
        mode=StartMode.NORMAL,
        data=data,
    )


async def cancel_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    user_id = cq.from_user.id
    await dialog_manager.done()
    keyboard = StartCandidateKeyboardButton(
        resize_keyboard=True,
        one_time_keyboard=True,
        is_persistent=True,
    )
    await cq.bot.send_message(
        chat_id=user_id,
        text="Отправка вопроса отменена.",
        reply_markup=keyboard(),
    )


async def question_back(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    data = dialog_manager.start_data
    data["offset"] = data.get("offset", 0) - 1
    await dialog_manager.switch_to(
        state=QuestionState.question_list,
    )


async def question_next(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    data = dialog_manager.start_data
    data["offset"] = data.get("offset", 0) + 1
    await dialog_manager.switch_to(
        state=QuestionState.question_list,
    )


@inject
async def question_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
        usecase: FromDishka[UserUseCase],
) -> None:
    data = dialog_manager.start_data.copy()
    item_id: str = dialog_manager.item_id  # noqa
    await dialog_manager.done()
    question_list = data.get("questions")
    question = question_list[int(item_id)]
    user_id = question.get("user_id")
    request = UserIDDTO(
        telegram_id=user_id,
    )
    user = await usecase.get(request)
    await dialog_manager.bg(
        user_id=cq.from_user.id,
        chat_id=cq.from_user.id,
    ).start(
        state=QuestionState.ask_question_director,
        mode=StartMode.NORMAL,
        data={
            "question_id": question.get("question_id"),
            "user_id": user_id,
            "question": question.get("question"),
            "username": user.full_name or f"@{user.username}",
        },
    )
