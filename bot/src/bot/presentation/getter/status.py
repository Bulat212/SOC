from typing import Any

from aiogram_dialog.api.entities import Context
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.application.dto.candidate import CandidateIDDTO
from bot.application.usecase.status import StatusUseCase


@inject
async def get_status(
        aiogd_context: Context,
        usecase: FromDishka[StatusUseCase],
        **kwargs: Any,
) -> dict[str, str]:
    data = aiogd_context.start_data
    request = CandidateIDDTO(
        telegram_id=str(data.get("user_id")),
    )
    status = await usecase.get(request)
    return {
        "status": status.status,
    }
