from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.adapter.db.model import BaseModel


class AnswerStorage(BaseModel):
    __tablename__ = "answers"

    question_id: Mapped[str] = mapped_column(
        ForeignKey("questions.id"),
        index=True,
    )
    answer: Mapped[str]
