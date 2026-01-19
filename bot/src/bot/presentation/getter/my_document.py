from dataclasses import asdict
from typing import Any

from aiogram import Bot
from aiogram.types import URLInputFile
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import Context, MediaAttachment
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.application.dto.candidate import (
    CandidateIDDTO,
)
from bot.application.usecase.candidate import CandidateUseCase


@inject
async def check_documents(
        aiogd_context: Context,
        dialog_manager: DialogManager,
        usecase: FromDishka[CandidateUseCase],
        **kwargs: Any,
) -> dict[str, bool]:
    data = aiogd_context.start_data
    request = CandidateIDDTO(
        telegram_id=data.get("user_id"),
    )
    candidate = await usecase.get_candidate(request)
    data = dict()
    for key, val in asdict(candidate).items():
        if key in ("is_form", "is_approval", "is_statement",):
            data[key] = val
            dialog_manager.start_data[key] = val
    return data


async def get_is_statement(
        aiogd_context: Context,
        **kwargs: Any,
) -> dict[str, bool]:
    data = aiogd_context.start_data
    return {
        "is_statement": data.get("is_statement"),
    }


async def get_is_form_sheet(
        aiogd_context: Context,
        **kwargs: Any,
) -> dict[str, bool]:
    data = aiogd_context.start_data
    return {
        "is_form": data.get("is_form"),
    }


async def get_is_approval(
        aiogd_context: Context,
        **kwargs: Any,
) -> dict[str, bool]:
    data = aiogd_context.start_data
    return {
        "is_approval": data.get("is_approval"),
    }
