from sqlalchemy import insert, select

from app.adapter.db.gateway.base import BaseGateway
from app.adapter.db.model import AnswerStorage
from app.domain.model import Answer


class AnswerDBGateway(BaseGateway[Answer]):
    async def insert(self, answer: Answer) -> Answer:
        query = (
            insert(
                AnswerStorage,
            )
            .values(
                id=answer.id,
                question_id=answer.question_id,
                answer=answer.answer,
            )
        )
        await self.session.execute(query)
        return answer

    async def get(self, answer_id: str) -> Answer | None:
        query = (
            select(
                AnswerStorage,
            )
            .where(
                AnswerStorage.id == answer_id,
            )
        )
        result = await self.session.execute(query)
        row = result.fetchone()
        if not row:
            return None
        return Answer(
            id=row.id,
            question_id=row.question_id,
            answer=row.answer,
        )
