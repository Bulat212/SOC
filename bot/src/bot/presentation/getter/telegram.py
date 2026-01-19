from typing import Any

from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.application.usecase.info import InfoUseCase
from bot.domain.exception.info import InfoNotFound


@inject
async def get_telegram_channel_url(
        usecase: FromDishka[InfoUseCase],
        **kwargs: Any,
) -> dict[str, str]:
    try:
        info = await usecase.get_info()
    except InfoNotFound:
        return {
            "error": "not found",
            "is_url": False,
        }
    return {
        "url": info.telegram_channel_url,
        "is_url": True
    }
