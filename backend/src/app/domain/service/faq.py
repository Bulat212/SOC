from dataclasses import asdict

from app.domain.exception.faq import FaqNotFound
from app.domain.model import Faq


class FaqService:
    def add_faq(self, faq_id: str, **data: dict[str, str]) -> Faq:
        faq = Faq(id=faq_id, **data)
        return faq

    def get(self, faq: Faq | None) -> dict[str, str]:
        if not faq:
            raise FaqNotFound()
        data = asdict(faq)
        return data
