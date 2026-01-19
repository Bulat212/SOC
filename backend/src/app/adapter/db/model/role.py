from sqlalchemy.orm import Mapped, mapped_column

from app.adapter.db.model import BaseModel


class RoleStorage(BaseModel):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(
        unique=True,
        index=True,
    )
