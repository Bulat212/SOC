from sqlalchemy.orm import Mapped, mapped_column

import datetime
from .base import BaseModel


class DelegateStorage(BaseModel):
    __tablename__ = "delegate"
    telegram_id: Mapped[str] = mapped_column(
        nullable=True,
        index=True,
        unique=True,
    )
    user_id: Mapped[str] = mapped_column(
        index=True,
    )
    first_name: Mapped[str] = mapped_column(
        nullable=True,
    )
    last_name: Mapped[str] = mapped_column(
        nullable=True,
    )
    patronymic: Mapped[str] = mapped_column(
        nullable=True,
    )
    post: Mapped[str] = mapped_column(
        nullable=True,
    )
    subject: Mapped[str] = mapped_column(
        default=None,
        nullable=True,
    )
    start_date: Mapped[datetime.date] = mapped_column(
        default=None,
        nullable=True,
    )
    end_date: Mapped[datetime.date] = mapped_column(
        default=None,
        nullable=True,
    )