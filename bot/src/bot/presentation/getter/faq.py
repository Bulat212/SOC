import math
from typing import Any

from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import Context
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.application.dto.faq import AddFaqDTO
from bot.application.dto.pagination import PaginationDTO
from bot.application.usecase.faq import FaqUseCase
from bot.constants import ZERO


@inject
async def get_faq_list(
        aiogd_context: Context,
        dialog_manager: DialogManager,
        usecase: FromDishka[FaqUseCase],
        **kwargs: Any,
) -> dict[str, str | int | list | bool]:
    data = aiogd_context.start_data
    request = PaginationDTO(
        limit=data.get("limit"),
        offset=data.get("offset"),
    )
    role = data.get("role")
    faq_list = await usecase.get_all(request)
    result = []
    attrs = ["id", "question", "answer"]
    for idx, val in enumerate(faq_list.values):
        data = dict()
        data["idx"] = idx
        for attr in attrs:
            data[attr] = getattr(val, attr, None)
        result.append(data)
    total_page = math.ceil(faq_list.total / faq_list.limit)
    is_back, is_next = True, True
    if total_page == 1:
        is_back, is_next = False, False
    elif total_page == request.offset + 1:
        is_back, is_next = True, False
    elif request.offset == ZERO:
        is_back, is_next = False, True
    dialog_manager.start_data["faq"] = result
    dialog_manager.start_data["role"] = role
    return {
        "total": faq_list.total,
        "faq": result,
        "page": faq_list.offset + 1,
        "pages": total_page,
        "is_faq": True if faq_list.total > 0 else False,
        "is_next": is_next,
        "is_back": is_back,
        "is_director": True if role == "director" else False,
    }


async def get_answer(
        aiogd_context: Context,
        **kwargs: Any,
) -> dict[str, str]:
    data = aiogd_context.start_data
    role = data.get("role")
    return {
        "question": data.get("question"),
        "answer": data.get("answer"),
        "is_director": True if role == "director" else False,
    }


@inject
async def add_faq(
        aiogd_context: Context,
        usecase: FromDishka[FaqUseCase],
        **kwargs: Any,
) -> dict[str, str]:
    data = aiogd_context.start_data
    request = AddFaqDTO(
        question=data.get("question"),
        answer=data.get("answer"),
    )
    await usecase.add(request)
    return {}
