from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.application.usecase.info import InfoUseCase
from bot.domain.exception.info import InfoNotFound


@inject
async def get_about_us(
        usecase: FromDishka[InfoUseCase],
        **kwargs,
) -> dict[str, str]:
    try:
        info = await usecase.get_info()
    except InfoNotFound:
        return {
            "error": "not_found",
            "is_url": False,
        }
    return {
        "url": info.about_us_url,
        "is_url": True,
    }
