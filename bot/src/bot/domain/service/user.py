from dataclasses import asdict
from typing import Any

from bot.domain.exception.user import UserNotFound
from bot.domain.model import User


class UserService:
    def get_user(self, user: User | None) -> dict[str, Any]:
        if not user:
            raise UserNotFound()
        return asdict(user)
