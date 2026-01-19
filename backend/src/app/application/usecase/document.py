from app.application.dto.document import (
    AddDocumentNameDTO,
    GetDocumentDTO,
    GetDocumentsNameDTO,
    GetDocumentNameDTO,
    AddDocumentDTO,
    GetPromoDocumentDTO,
)
from app.application.interface.db import DBSession
from app.application.interface.gateway.document import (
    IPromoDocumentDBGateway,
    IDocumentDBGateway,
)
from app.application.interface.gateway.info import IInfoDBGateway
from app.application.interface.s3.client import IMinIOClient
from app.application.interface.ulid_generator import ULIDGenerator
from app.config import ApplicationConfig
from app.domain.service.document import PromoDocumentService, DocumentService
from app.domain.service.info import InfoService


class PromoDocumentUseCase:
    def __init__(
            self,
            promo_document_db_gateway: IPromoDocumentDBGateway,
            info_db_gateway: IInfoDBGateway,
            info_service: InfoService,
            promo_document_service: PromoDocumentService,
            ulid_generator: ULIDGenerator,
            minio: IMinIOClient,
            config: ApplicationConfig,
            db_session: DBSession,
    ) -> None:
        self.promo_document_db_gateway = promo_document_db_gateway
        self.info_db_gateway = info_db_gateway
        self.info_service = info_service
        self.promo_document_service = promo_document_service
        self.ulid_generator = ulid_generator
        self.minio = minio
        self.config = config
        self.db_session = db_session

    async def get(
            self,
            request: AddDocumentNameDTO,
    ) -> GetPromoDocumentDTO:
        info = await self.info_db_gateway.get()
        info_id = self.info_service.get_info_id(info)
        document = await self.promo_document_db_gateway.get(
            info_id=info_id,
            name=request.name,
        )
        data = self.promo_document_service.get_document(document)
        return GetPromoDocumentDTO(**data)

    async def get_name_all(self) -> GetDocumentsNameDTO:
        # TODO: Добавить пагинацию
        name_list = await self.promo_document_db_gateway.get_name_all()
        result = []
        for val in name_list:
            result.append(
                GetDocumentNameDTO(
                    name=val,
                ),
            )
        return GetDocumentsNameDTO(
            values=result,
        )

    async def add(self, request: AddDocumentDTO) -> GetPromoDocumentDTO:
        info = await self.info_db_gateway.get()
        info_id = self.info_service.get_info_id(info)
        url = self.promo_document_service.generate_url(
            url=self.config.s3.endpoint,
            bucket=self.config.s3.promo_bucket,
            filename=request.filename,
            name=request.name,
        )
        path = self.promo_document_service.generate_path(
            filename=request.filename,
            name=request.name,
        )
        file = self.promo_document_service.get_file(request.file)
        await self.minio.put_object(
            bucket=self.config.s3.promo_bucket,
            key=path,
            file=file,
        )
        document = self.promo_document_service.add_document(
            document_id=str(self.ulid_generator()),
            info_id=info_id,
            name=request.name,
            url=url,
        )
        await self.promo_document_db_gateway.insert(document)
        await self.db_session.commit()
        data = self.promo_document_service.get_document(document)
        return GetPromoDocumentDTO(**data)

    async def delete(self, request: AddDocumentNameDTO) -> None:
        info = await self.info_db_gateway.get()
        info_id = self.info_service.get_info_id(info)
        document = await self.promo_document_db_gateway.get(
            info_id=info_id,
            name=request.name,
        )
        data = self.promo_document_service.get_document(document)
        path = self.promo_document_service.get_path(
            endpoint=self.config.s3.endpoint,
            url=data.get("url"),
            bucket_name=self.config.s3.promo_bucket,
        )
        await self.minio.delete_object(
            bucket=self.config.s3.promo_bucket,
            key=path,
        )
        await self.promo_document_db_gateway.delete(
            name=request.name,
        )
        await self.db_session.commit()


class DocumentUseCase:
    def __init__(
            self,
            document_db_gateway: IDocumentDBGateway,
            info_db_gateway: IInfoDBGateway,
            info_service: InfoService,
            document_service: DocumentService,
    ) -> None:
        self.document_db_gateway = document_db_gateway
        self.info_db_gateway = info_db_gateway
        self.info_service = info_service
        self.document_service = document_service

    async def get(
            self,
            request: AddDocumentNameDTO,
    ) -> GetDocumentDTO:
        info = await self.info_db_gateway.get()
        info_id = self.info_service.get_info_id(info)
        document = await self.document_db_gateway.get(
            info_id=info_id,
            name=request.name,
        )
        data = self.document_service.get_document(document)
        return GetDocumentDTO(**data)
