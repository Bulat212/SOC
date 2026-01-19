from sqlalchemy.orm import Mapped, mapped_column

from app.adapter.db.model import BaseModel


class QuestionStorage(BaseModel):
    __tablename__ = "questions"

    number: Mapped[int] = mapped_column(
        nullable=True,
    )
    user_id: Mapped[str] = mapped_column(
        index=True,
    )
    question: Mapped[str]
    is_answer: Mapped[bool]
