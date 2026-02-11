from typing import Any
from bot.application.dto.pagination import PaginationDTO
from bot.application.usecase.recruitment import RecruitmentUseCase

from aiogram_dialog import DialogManager
from bot.application.usecase.candidate import CandidateUseCase
from bot.adapter.broker.gateway.candidate import CandidateBrokerGateway

from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject


@inject
async def get_candidates_list(dialog_manager: DialogManager, usecase: FromDishka[CandidateUseCase], **kwargs):
    data = dialog_manager.dialog_data
    recruitment = data.get("recruitment")
    recruitment_id = recruitment["id"]
    # Если нет текущей страницы — ставим 0
    page = data.get("page", 0)
    limit = 2
    offset = page * limit
    is_candidate=True

    candidate_list = await usecase.get_candidates_by_recruitment(
        recruitment_id=recruitment_id,
        limit=limit,
        offset=offset,
    )

    if len(candidate_list)==0:
        is_candidate=False
    else:
        total = candidate_list[-1].get('total')
    del candidate_list[-1]
    total_pages = (total + limit - 1) // limit

     # Вычисляем кнопки
    is_back = page > 0
    is_next = page + 1 < total_pages  # следующая страница есть, если не последняя
    # Сохраняем данные в start_data
    dialog_manager.dialog_data["page"] = page
    dialog_manager.dialog_data["is_next"] = is_next
    dialog_manager.dialog_data["is_back"] = is_back
    dialog_manager.dialog_data["current_candidates"] = candidate_list

    return {
        "recruitment_name": recruitment["name"],
        "candidates": candidate_list,
        "is_next": is_next,
        "is_back": is_back,
        "page": page + 1,
        "pages": total_pages,
        "total": total,
        "is_candidate": is_candidate,
    }


@inject
async def get_recruitments(
        usecase: FromDishka[RecruitmentUseCase],
        dialog_manager: DialogManager,
        **kwargs: Any,
) -> dict[str, list[str]]: 
    recruitments = await usecase.all()
    result = []
    for idx, val in enumerate(recruitments.values):
        result.append(
            {
                "idx": idx,
                "id": val.id,
                "name": val.name,
            },
        )

    dialog_manager.dialog_data["recruitments"] = result
    return {
        "recruitments": result,
    }