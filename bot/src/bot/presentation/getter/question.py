import math
from typing import Any

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import Context
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.application.dto.pagination import PaginationDTO
from bot.application.dto.question import AddQuestionDTO
from bot.application.usecase.question import QuestionUseCase
from bot.config import BotConfig
from bot.constants import ZERO


async def get_user_question(
        aiogd_context: Context,
        **kwargs: Any,
) -> dict[str, str]:
    data = aiogd_context.start_data
    return {
        "name": data.get("username"),
        "question": data.get("question"),
    }


@inject
async def get_question(
        bot: Bot,
        aiogd_context: Context,
        usecase: FromDishka[QuestionUseCase],
        config: FromDishka[BotConfig],
        **kwargs: Any,
) -> dict[str, str]:
    data = aiogd_context.start_data
    request = AddQuestionDTO(
        telegram_id=str(data.get("user_id")),
        question=data.get("question"),
    )
    question = await usecase.add(request)
    number = question.id[:6] if question.number is None else question.number
    if config.group_id:
        try:
            await bot.send_message(
                chat_id=config.group_id,
                text="{name} направил вопрос №{number}:\n\n «<i><u>{question}</u></i>»".format(
                    name=data.get("username"),
                    question=data.get("question"),
                    number=number,
                ),
                message_thread_id=config.questions_topic_id,
            )
        except TelegramBadRequest:
            pass
    aiogd_context.start_data["question_id"] = question.id
    return {
        "question": data.get("question"),
        "number": number,
    }


@inject
async def get_questions(
        aiogd_context: Context,
        dialog_manager: DialogManager,
        usecase: FromDishka[QuestionUseCase],
        **kwargs: Any,
) -> dict[str, str | int | list | bool]:
    data = aiogd_context.start_data
    request = PaginationDTO(
        limit=data.get("limit"),
        offset=data.get("offset"),
    )
    question_list = await usecase.get_all(request)
    result = []
    attrs = ["id", "question", "is_answer", "user_id"]
    for idx, val in enumerate(question_list.values):
        data = dict()
        data["idx"] = idx
        for attr in attrs:
            if attr == "id":
                data["question_id"] = getattr(val, attr, None)
                continue
            data[attr] = getattr(val, attr, None)
        result.append(data)
    total_page = math.ceil(question_list.total / question_list.limit)
    is_back, is_next = True, True
    if total_page == 1:
        is_back, is_next = False, False
    elif total_page == request.offset + 1:
        is_back, is_next = True, False
    elif request.offset == ZERO:
        is_back, is_next = False, True
    dialog_manager.start_data["questions"] = result
    return {
        "total": question_list.total,
        "questions": result,
        "page": question_list.offset + 1,
        "pages": total_page,
        "is_question": True if question_list.total > 0 else False,
        "is_next": is_next,
        "is_back": is_back,
    }
