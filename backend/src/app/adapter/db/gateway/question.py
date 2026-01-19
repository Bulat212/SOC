from collections.abc import AsyncIterable
from dataclasses import asdict

from sqlalchemy import insert, select, update, func, desc, null

from app.adapter.db.gateway.base import BaseGateway
from app.adapter.db.model import QuestionStorage
from app.domain.model import Question


class QuestionDBGateway(BaseGateway[Question]):
    async def insert(self, question: Question) -> Question:
        stmt = (
            insert(QuestionStorage)
            .values(**asdict(question))
        )
        await self.session.execute(stmt)
        return question

    async def get(self, question_id: str) -> Question | None:
        stmt = (
            select(QuestionStorage)
            .where(QuestionStorage.id == question_id)
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            return None
        return Question(
            id=model.id,
            user_id=model.user_id,
            question=model.question,
            number=model.number,
            is_answer=model.is_answer,
        )

    async def all(self, limit: int, offset: int) -> AsyncIterable[Question]:
        stmt = (
            select(QuestionStorage)
            .where(QuestionStorage.is_answer == False)
            .limit(limit)
            .offset(offset)
            .order_by(desc(QuestionStorage.id))
        )
        result = await self.session.execute(stmt)
        for val in result.scalars():
            yield Question(
                id=val.id,
                user_id=val.user_id,
                question=val.question,
                number=val.number,
                is_answer=val.is_answer,
            )

    async def get_total(self) -> int:
        stmt = (
            select(func.count(QuestionStorage.id))
            .where(QuestionStorage.is_answer == False)
        )
        result = await self.session.scalar(stmt)
        return result

    async def change_status(self, question_id: str, is_answer: bool) -> None:
        stmt = (
            update(QuestionStorage)
            .where(QuestionStorage.id == question_id)
            .values(is_answer=is_answer)
            .returning(QuestionStorage)
        )
        await self.session.execute(stmt)

    async def get_number(self) -> int | None:
        stmt = (
            select(func.coalesce(func.max(QuestionStorage.number), 0))
            .where(QuestionStorage.number != null())
        )
        result = await self.session.execute(stmt)
        return result.scalar()
