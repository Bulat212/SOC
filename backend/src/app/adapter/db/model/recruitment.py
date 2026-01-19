from sqlalchemy.orm import Mapped

from app.adapter.db.model import BaseModel


class RecruitmentStorage(BaseModel):
    __tablename__ = "recruitment"

    name: Mapped[str]
