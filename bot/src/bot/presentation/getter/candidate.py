from dataclasses import asdict
from typing import Any

from aiogram_dialog.api.entities import Context
from bot.presentation.button.start_button import DeleteCandidateDataKeyboardButton, StartDelegateKeyboardButton
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from aiogram_dialog import DialogManager
from aiogram.types import Message

from bot.application.dto.candidate import CandidateIDDTO
from bot.application.usecase.candidate import CandidateUseCase


@inject
async def get_candidate(
        aiogd_context: Context,
        usecase: FromDishka[CandidateUseCase],
        **kwargs: Any,
) -> dict[str, str | bool]:
    data = aiogd_context.start_data
    if data.get("is_request"):
        request = CandidateIDDTO(
            telegram_id=data.get("telegram_id"),
        )
        candidate = await usecase.get_candidate(request)
        del data["is_request"]
        for key, value in asdict(candidate).items():
            if key in ["birthdate", "graduation_date"]:
                value = value.strftime("%d.%m.%Y")
            data[key] = value
        return {
            "recruitment": candidate.recruitment,
            "first_name": candidate.first_name,
            "last_name": candidate.last_name,
            "patronymic": candidate.patronymic,
            "birthdate": candidate.birthdate.strftime("%d.%m.%Y"),
            "subject": candidate.subject,
            "nationality": candidate.nationality,
            "military_station": candidate.military_station,
            "military_station_address": candidate.military_station_address,
            "university": candidate.university,
            "direction_training": candidate.direction_training,
            "average_score": candidate.average_score,
            "phone_number": candidate.phone_number,
            "find_out": candidate.find_out,
            "graduation_date": candidate.graduation_date.strftime("%d.%m.%Y"),
            "is_save": False,
            "is_edit": data.get("is_edit"),
        }
    try:
        recruitment = data.get("recruitment").get("name")
    except AttributeError:
        recruitment = data.get("recruitment")
    return {
        "recruitment": recruitment,
        "first_name": data.get("first_name"),
        "last_name": data.get("last_name"),
        "patronymic": data.get("patronymic"),
        "birthdate": data.get("birthdate"),
        "subject": data.get("subject"),
        "nationality": data.get("nationality"),
        "military_station": data.get("military_station"),
        "military_station_address": data.get("military_station_address"),
        "university": data.get("university"),
        "direction_training": data.get("direction_training"),
        "average_score": data.get("average_score"),
        "phone_number": data.get("phone_number"),
        "find_out": data.get("find_out"),
        "graduation_date": data.get("graduation_date"),
        "is_save": data.get("is_save"),
        "is_edit": data.get("is_edit", False),
    }


@inject
async def delete_candidate(
        aiogd_context: Context,
        message: Message,
        dialog_manager: DialogManager,
        usecase: FromDishka[CandidateUseCase],
        **kwargs: Any,
) -> dict[str, str | bool]:
    keyboard = DeleteCandidateDataKeyboardButton(
                        resize_keyboard=True,
                        one_time_keyboard=False,
                        is_persistent=True,
                    )
    await message.answer(
                text="Введите следующий текст", 
                reply_markup=keyboard(),
            )
    
    data = aiogd_context.start_data

    return {
        "recruitment": "recruitment",
    }


