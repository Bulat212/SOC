from dataclasses import asdict

from app.domain.exception.user import UserNotFound
from app.domain.model import User


class UserService:
    def add_user(self, **data: str | bool) -> User:
        user = User(
            id=data.get("id"),
            telegram_id=data.get("telegram_id"),
            username=data.get("username"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            role_id=data.get("role_id"),
        )
        return user

    def get_user(self, user: User | None) -> dict[str, str | bool]:
        if not user:
            raise UserNotFound()
        return asdict(user)

    def get_user_id(self, user: User | None) -> str:
        if not user:
            raise UserNotFound()
        return user.id

    def get_user_telegram_id(self, user: User | None) -> str:
        if not user:
            raise UserNotFound()
        return user.telegram_id
