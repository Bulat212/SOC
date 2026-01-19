from typing import Any

from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.application.usecase.recruitment import RecruitmentUseCase


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
                "idx": idx,
                "id": val.id,
                "name": val.name,
            },
        )
    dialog_manager.start_data["recruitments"] = result
    return {
        "recruitments": result,
    }
