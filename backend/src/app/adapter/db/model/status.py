from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.adapter.db.model import BaseModel


class StatusStorage(BaseModel):
    __tablename__ = "statuses"

    candidate_id: Mapped[str] = mapped_column(
        ForeignKey("candidates.id"),
        index=True,
        unique=True,
    )
    status: Mapped[str]
