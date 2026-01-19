from sqlalchemy import select

from app.adapter.db.gateway.base import BaseGateway
from app.adapter.db.model import RecruitmentStorage
from app.domain.model import Recruitment


class RecruitmentDBGateway(BaseGateway[Recruitment]):
    async def all(self) -> list[Recruitment]:
        stmt = (
            select(RecruitmentStorage)
        )
        result = await self.session.execute(stmt)
        return [
            Recruitment(
                id=val.id,
                name=val.name,
            )
            for val in result.scalars()
        ]

    async def get(self, recruitment_id: str) -> Recruitment | None:
        stmt = (
            select(RecruitmentStorage)
            .where(
                RecruitmentStorage.id == recruitment_id,
            )
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            return None
        return Recruitment(
            id=model.id,
            name=model.name,
        )
