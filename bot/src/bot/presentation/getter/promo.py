import os
from typing import Any

from aiogram import Bot
from aiogram_dialog.api.entities import Context
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.application.dto.document import AddDocumentDTO
from bot.application.usecase.promo import PromoUseCase


@inject
async def get_promo_documents_name(
        aiogd_context: Context,
        usecase: FromDishka[PromoUseCase],
        **kwargs: Any,
) -> dict[str, list[str | int]]:
    data = aiogd_context.start_data
    name_list = await usecase.get_name_all()
    role = data.get("role")
    result = []
    attrs = ["name"]
    for idx, val in enumerate(name_list.values):
        data = dict()
        data["idx"] = idx
        for attr in attrs:
            data[attr] = getattr(val, attr)
        result.append(data)
    aiogd_context.start_data["role"] = role
    aiogd_context.start_data["promo"] = result
    return {
        "promo": result,
        "is_director": True if role == "director" else False,
        "is_promo": True if len(name_list.values) > 0 else False,
    }


@inject
async def add_promo_document(
        bot: Bot,
        aiogd_context: Context,
        usecase: FromDishka[PromoUseCase],
        **kwargs: Any,
) -> dict:
    data = aiogd_context.start_data
    name = data.get("name")
    file_path = data.get("file_path")
    filename = file_path.split("/")[-1]
    file = await bot.download_file(
        file_path=file_path,
    )
    file.seek(os.SEEK_SET)
    request = AddDocumentDTO(
        name=name,
        file=file.read(),
        filename=filename,
    )
    await usecase.add(request)
    return {}
