from typing import Any

from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.application.usecase.recruitment import RecruitmentUseCase
from bot.presentation.utils.candidate import filter_recruitments_by_date


@inject
async def check_recruitments(
        usecase: FromDishka[RecruitmentUseCase],
        **kwargs: Any,
) -> dict[str, bool]:
    is_recruitments = await usecase.check_recruitments()
    return {
        "is_recruitments": is_recruitments,
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
                "id": val.id,
                "name": val.name,
            },
        )

    filtered_result = filter_recruitments_by_date(result)
    result_with_idx = []
    for idx, val in enumerate(filtered_result):
        result_with_idx.append(
            {
                "idx": idx,
                "id": val.get("id"),
                "name": val.get("name"),
            },
        )
    dialog_manager.start_data["recruitments"] = result_with_idx
    return {"recruitments": result_with_idx}
