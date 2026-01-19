from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    id: Mapped[str] = mapped_column(
        primary_key=True,
        nullable=False,
        unique=True,
        autoincrement=False,
    )
