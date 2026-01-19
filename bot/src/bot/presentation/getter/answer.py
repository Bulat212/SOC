from typing import Any

from aiogram_dialog.api.entities import Context


async def get_answer(
        aiogd_context: Context,
        **kwargs: Any,
) -> dict[str, str]:
    data = aiogd_context.start_data
    return {
        "question": data.get("question"),
        "answer": data.get("answer"),
    }
