from dataclasses import asdict

from bot.domain.exception.faq import FaqNotFound
from bot.domain.model.faq import Faq, FaqList


class FaqService:
    def add_faq(self, **data: dict[str, str]) -> Faq:
        faq = Faq(**data)
        return faq

    def get_faq(self, faq: Faq | None) -> dict[str, None]:
        if not faq:
            raise FaqNotFound()
        data = asdict(faq)
        return data

    def get_faq_list(
            self,
            faq_list: FaqList | None,
    ) -> dict[str, str | int | list[dict[str, str]]]:
        if not faq_list:
            raise FaqNotFound()
        data = asdict(faq_list)
        return data
