from dataclasses import asdict
from sqlalchemy import text, insert, select, update

from app.adapter.db.gateway.base import BaseGateway
from app.adapter.db.model import DelegateStorage
from app.domain.model import Delegate


class DelegateDBGateway(BaseGateway[Delegate]):
    async def insert(self, delegate: Delegate) -> Delegate:
        data = dict()
        for key, val in asdict(delegate).items():
            data[key] = val
        stmt = (
            insert(DelegateStorage)
            .values(**data)
        )
        await self.session.execute(stmt)
        return delegate
    

    async def get(self, telegram_id: str) -> Delegate | None:
        query = (
            select(
                DelegateStorage,
            )
            .where(
                DelegateStorage.telegram_id == telegram_id,
            )
        )
        result = await self.session.execute(query)
        model = result.scalar_one_or_none()
        if not model:
            return None
      
        return Delegate(
            id=model.id,       
            user_id=model.user_id, 
            telegram_id=model.telegram_id,
            first_name=model.first_name,
            last_name=model.last_name,
            patronymic=model.patronymic,
            post=model.post,
            subject=model.subject,
            start_date=model.start_date,
            end_date=model.end_date,
        )
    

    async def update(self, delegate: DelegateStorage) -> DelegateStorage:
        stmt = (
            update(DelegateStorage)
            .values(**(asdict(delegate)))
            .where(DelegateStorage.telegram_id == delegate.telegram_id)
        )
        await self.session.execute(stmt)
        return delegate


class AnswerGateway(BaseGateway):
    async def get(self, delegate_id: str) -> Delegate | None:
        query = (
            select(
                DelegateStorage,
            )
            .where(
                DelegateStorage.id == delegate_id,
            )
        )
        result = await self._session.execute(query)
        row = result.fetchone()
        if not row:
            return None
        return Delegate(
            id=row.id,       
            user_id=row.user_id, 
            first_name=row.first_name,
            last_name=row.last_name,
            patronymic=row.patronymic
        )