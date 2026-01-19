from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.adapter.db.model import BaseModel


class DocumentStorage(BaseModel):
    __tablename__ = "documents"

    name: Mapped[str]
    url: Mapped[str]
    info_id: Mapped[str] = mapped_column(
        ForeignKey("info.id"),
        index=True,
    )


class PromoDocumentStorage(BaseModel):
    __tablename__ = "promo_documents"

    name: Mapped[str]
    url: Mapped[str]
    info_id: Mapped[str] = mapped_column(
        ForeignKey("info.id"),
        index=True,
    )
    is_active: Mapped[bool] = mapped_column(
        default=True,
        server_default="true",
    )
