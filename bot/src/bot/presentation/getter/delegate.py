from dataclasses import asdict
from typing import Any

from aiogram_dialog.api.entities import Context
from bot.application.dto.delegate import DelegateIDDTO
from bot.application.usecase.delegate import DelegateUseCase
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject




@inject
async def get_delegate(
        aiogd_context: Context,
        usecase: FromDishka[DelegateUseCase],
        **kwargs: Any,
) -> dict[str, str | bool]:
    data = aiogd_context.start_data
    if data.get("is_request"):
        request = DelegateIDDTO(
            telegram_id=data.get("telegram_id"),
        )
        delegate = await usecase.get(request)
        del data["is_request"]
        for key, value in asdict(delegate).items():
            if key in ["start_date", "end_date"] and value:
                value = value.strftime("%d.%m.%Y")
            data[key] = value
        return {
            "first_name": delegate.first_name,
            "last_name": delegate.last_name,
            "patronymic": delegate.patronymic,
            "subject": delegate.subject,
            "post": delegate.post,
            "start_date": delegate.start_date.strftime("%d.%m.%Y") if delegate.start_date else None,
            "end_date": delegate.end_date.strftime("%d.%m.%Y") if delegate.end_date else None,
            "is_save": False,
            "is_edit": data.get("is_edit"),
        }
    return {
        "first_name": data.get("first_name"),
        "last_name": data.get("last_name"),
        "patronymic": data.get("patronymic"),
        "subject": data.get("subject"),
        "post": data.get("post"),
        "start_date": data.get("start_date"),
        "end_date": data.get("end_date"),
        "is_save": data.get("is_save"),
        "is_edit": data.get("is_edit", False),
    }
