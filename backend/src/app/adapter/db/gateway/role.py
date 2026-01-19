from sqlalchemy import select

from app.adapter.db.gateway.base import BaseGateway
from app.adapter.db.model.role import RoleStorage
from app.domain.model import Role
from app.domain.model.role import RoleEnum


class RoleDBGateway(BaseGateway[Role]):
    async def get(self, role_id: str) -> Role | None:
        stmt = (
            select(RoleStorage)
            .where(RoleStorage.id == role_id)
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            return None
        return Role(
            id=model.id,
            name=RoleEnum(model.name),
        )

    async def get_role(self, name: str) -> Role | None:
        stmt = (
            select(RoleStorage)
            .where(RoleStorage.name == name)
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            return None
        return Role(
            id=model.id,
            name=RoleEnum(model.name),
        )
