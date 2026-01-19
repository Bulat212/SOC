from sqlalchemy.orm import Mapped

from app.adapter.db.model import BaseModel


class FaqStorage(BaseModel):
    __tablename__ = "faq"
    
    question: Mapped[str]
    answer: Mapped[str]
