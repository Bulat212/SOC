from dataclasses import asdict
from urllib.parse import quote, urljoin
import base64
from app.domain.exception.document import DocumentNotFound
from app.domain.model import Document
from app.domain.model.document import PromoDocument


class PromoDocumentService:
    def get_path(self, endpoint: str, url: str, bucket_name: str) -> str:
        path = url.replace(f"{endpoint}/", "").replace(f"{bucket_name}/", "")
        return path

    def get_file(self, file: str) -> bytes:
        return base64.b64decode(file)

    def generate_url(self,
            url: str,
            bucket: str,
            filename: str,
            name: str,
    ) -> str:
        # TODO: Сделать более безопасный способ
        file_extension = filename.split('.')[-1]
        filename = f"{name}.{file_extension}"
        bucket_quote = quote(bucket, safe='')
        filename = quote(filename, safe='')
        full_url = urljoin(url.rstrip("/") + "/", f"{bucket_quote}/{filename}")
        return full_url

    def generate_path(
            self,
            filename: str,
            name: str,
    ) -> str:
        file_extension = filename.split('.')[-1]
        filename = f"{name}.{file_extension}"
        return filename

    def add_document(self, document_id: str, **data: str) -> PromoDocument:
        document = PromoDocument(
            id=document_id,
            **data,
        )
        return document

    def get_document(self, document: PromoDocument | None) -> dict[str, str]:
        if not document:
            raise DocumentNotFound()
        data = asdict(document)
        del data["info_id"]
        return data


class DocumentService:
    def get_document(self, document: Document | None) -> dict[str, str]:
        if not document:
            raise DocumentNotFound()
        data = asdict(document)
        del data["info_id"]
        return data
