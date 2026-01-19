import base64
from dataclasses import asdict

from bot.domain.exception.document import DocumentNotFound
from bot.domain.model.document import Document


class PromoService:
    def get_promo(self, document: Document | None) -> dict[str, str]:
        if not document:
            raise DocumentNotFound()
        data = asdict(document)
        return data

    def to_file_base64(self, file: bytes) -> str:
        return base64.b64encode(file).decode()
