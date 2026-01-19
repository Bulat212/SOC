from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.adapter.db.model import BaseModel


class UserStorage(BaseModel):
    __tablename__ = "users"

    telegram_id: Mapped[str] = mapped_column(
        index=True,
    )
    username: Mapped[str] = mapped_column(nullable=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    role_id: Mapped[str] = mapped_column(
        ForeignKey("roles.id"),
        index=True,
    )
    is_active: Mapped[bool] = mapped_column(
        default=False,
    )
