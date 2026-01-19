from collections.abc import AsyncIterable
from dataclasses import asdict

from sqlalchemy import select, func, insert, delete

from app.adapter.db.gateway.base import BaseGateway
from app.adapter.db.model import FaqStorage
from app.domain.model import Faq


class FaqDBGateway(BaseGateway[Faq]):
    async def get(self, faq_id: str) -> Faq | None:
        stmt = (
            select(FaqStorage)
            .where(FaqStorage.id == faq_id)
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            return None
        return Faq(
            id=model.id,
            question=model.question,
            answer=model.answer,
        )

    async def all(self, limit: int, offset: int) -> AsyncIterable[Faq]:
        stmt = (
            select(FaqStorage)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        for val in result.scalars():
            yield Faq(
                id=val.id,
                question=val.question,
                answer=val.answer,
            )

    async def get_total(self) -> int:
        stmt = (
            select(func.count(FaqStorage.id))
        )
        result = await self.session.scalar(stmt)
        return result

    async def insert(self, faq: Faq) -> Faq:
        stmt = (
            insert(FaqStorage)
            .values(**asdict(faq))
        )
        await self.session.execute(stmt)
        return faq

    async def delete(self, faq_id: str) -> None:
        stmt = (
            delete(FaqStorage)
            .where(FaqStorage.id == faq_id)
        )
        await self.session.execute(stmt)
