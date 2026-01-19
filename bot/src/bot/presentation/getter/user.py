from typing import Any

from aiogram_dialog.api.entities import Context


async def get_user(
        aiogd_context: Context,
        **kwargs: Any,
) -> dict[str, str]:
    data = aiogd_context.start_data
    return {
        "username": data.get("username"),
        "role": data.get("role"),
    }
