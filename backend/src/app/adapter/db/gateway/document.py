from dataclasses import asdict

from sqlalchemy import select, and_, insert, delete

from app.adapter.db.gateway.base import BaseGateway
from app.adapter.db.model import PromoDocumentStorage, DocumentStorage
from app.domain.model import Document
from app.domain.model.document import PromoDocument


class PromoDocumentDBGateway(BaseGateway[PromoDocument]):
    async def delete(self, name: str) -> None:
        stmt = (
            delete(PromoDocumentStorage)
            .where(PromoDocumentStorage.name == name)
        )
        await self.session.execute(stmt)

    async def get(
            self,
            info_id: str,
            name: str,
    ) -> PromoDocument | None:
        stmt = (
            select(PromoDocumentStorage)
            .where(
                and_(
                    PromoDocumentStorage.info_id == info_id,
                    PromoDocumentStorage.name == name,
                ),
            )
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            return None
        return PromoDocument(
            id=model.id,
            name=model.name,
            url=model.url,
            info_id=model.info_id,
            is_active=model.is_active,
        )

    async def insert(self, document: PromoDocument) -> PromoDocument:
        stmt = (
            insert(PromoDocumentStorage)
            .values(**asdict(document))
        )
        await self.session.execute(stmt)
        return document

    async def get_name_all(self) -> list[str]:
        # TODO: Добавить limit и offset
        stmt = (
            select(PromoDocumentStorage)
            .where(
                PromoDocumentStorage.is_active == True,
            )
        )
        result = await self.session.execute(stmt)
        return [val.name for val in result.scalars()]


class DocumentDBGateway(BaseGateway[Document]):
    async def get(
            self,
            info_id: str,
            name: str,
    ) -> Document | None:
        stmt = (
            select(DocumentStorage)
            .where(
                and_(
                    DocumentStorage.info_id == info_id,
                    DocumentStorage.name == name,
                ),
            )
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            return None
        return Document(
            id=model.id,
            name=model.name,
            url=model.url,
            info_id=model.info_id,
        )
