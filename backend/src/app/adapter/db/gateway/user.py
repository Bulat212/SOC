from dataclasses import asdict

from sqlalchemy import select, or_, insert, delete

from app.adapter.db.gateway.base import BaseGateway
from app.adapter.db.model import UserStorage
from app.domain.model import User


class UserDBGateway(BaseGateway[User]):
    async def insert(self, user: User) -> User:
        stmt = (
            insert(UserStorage)
            .values(**asdict(user))
        )
        await self.session.execute(stmt)
        return user

    async def get(
            self,
            user_id: str | None = None,
            telegram_id: str | None = None,
    ) -> User | None:
        stmt = (
            select(UserStorage)
            .where(
                or_(
                    UserStorage.telegram_id == telegram_id,
                    UserStorage.id == user_id,
                ),
            )
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            return None
        return User(
            id=model.id,
            telegram_id=model.telegram_id,
            username=model.username,
            first_name=model.first_name,
            last_name=model.last_name,
            role_id=model.role_id,
            is_active=model.is_active,
        )

    async def get_id_all(self, role_id: str) -> list[str]:
        stmt = (
            select(UserStorage)
            .where(
                UserStorage.role_id == role_id,
            )
        )
        result = await self.session.execute(stmt)
        return [val.telegram_id for val in result.scalars()]

    async def delete(self, user_id: str):
        stmt = (
            delete(UserStorage)
            .where(UserStorage.id == user_id)
        )
        await self.session.execute(stmt)