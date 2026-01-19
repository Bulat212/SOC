from dataclasses import asdict

from sqlalchemy import insert, select, delete

from app.adapter.db.gateway.base import BaseGateway
from app.adapter.db.model import StatusStorage
from app.domain.model import Status
from app.domain.model.status import StatusEnum


class StatusDBGateway(BaseGateway[Status]):
    async def get(self, candidate_id: str) -> Status | None:
        stmt = (
            select(StatusStorage)
            .where(StatusStorage.candidate_id == candidate_id)
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            return None
        return Status(
            id=model.id,
            candidate_id=model.candidate_id,
            status=StatusEnum(model.status),
        )

    async def insert(self, status: Status) -> Status:
        stmt = (
            insert(StatusStorage)
            .values(**asdict(status))
        )
        await self.session.execute(stmt)
        return status

    async def delete(self, candidate_id: str): 
        stmt = (
            delete(StatusStorage)
            .where(StatusStorage.candidate_id == candidate_id)
        )
        await self.session.execute(stmt)