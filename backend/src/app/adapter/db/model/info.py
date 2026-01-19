from sqlalchemy.orm import Mapped, mapped_column

from app.adapter.db.model import BaseModel


class InfoStorage(BaseModel):
    __tablename__ = "info"

    about_us_url: Mapped[str] = mapped_column(
        nullable=True,
        index=True,
    )
    telegram_channel_url: Mapped[str] = mapped_column(
        nullable=True,
        index=True,
    )
    is_info: Mapped[bool]
