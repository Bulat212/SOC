from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from app.adapter.db.model import BaseModel


class IDocument(BaseModel):
    __abstract__ = True

    name: Mapped[str] = mapped_column(
        index=True,
    )
    url: Mapped[str]
