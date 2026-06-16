import asyncio
import io
from dataclasses import asdict
from typing import Any

from app.application.dto.candidate import (
    AddCandidateDTO,
    FormDataDTO,
    GetCandidateDTO,
    AddCandidateIDDTO,
    GetCandidatesDTO,
    UpdateCandidateDTO,
    CandidateDocumentNameDTO,
)
from app.application.dto.document import (
    GetDocumentDTO,
    UpdateDocumentDTO,
)
from app.application.dto.pagination import PaginationDTO
from app.application.interface.db import DBSession
from app.application.interface.document.template import ITemplate
from app.application.interface.gateway.candidate import (
    ICandidateDBGateway,
    ICandidateFormDBGateway,
    ICandidateApprovalDBGateway,
    ICandidateStatementDBGateway,
    ICandidateYandexFormGateway,
)
from app.application.interface.gateway.recruitment import IRecruitmentDBGateway
from app.application.interface.gateway.role import IRoleDBGateway
from app.application.interface.gateway.status import IStatusDBGateway
from app.application.interface.gateway.user import IUserDBGateway
from app.application.interface.s3.client import IMinIOClient
from app.application.interface.ulid_generator import ULIDGenerator
from app.config import ApplicationConfig
from app.domain.model import CandidateDocument
from app.domain.model.role import RoleEnum
from app.domain.service.candidate import (
    CandidateService,
)
from app.domain.service.status import StatusService
from app.domain.service.user import UserService
from faststream.rabbit import RabbitBroker

class CandidateUseCase:
    def __init__(
            self,
            candidate_db_gateway: ICandidateDBGateway,
            candidate_yandex_form_db_gateway: ICandidateYandexFormGateway,
            candidate_form_db_gateway: ICandidateFormDBGateway,
            candidate_approval_db_gateway: ICandidateApprovalDBGateway,
            candidate_statement_db_gateway: ICandidateStatementDBGateway,
            broker: RabbitBroker,
            user_db_gateway: IUserDBGateway,
            role_db_gateway: IRoleDBGateway,
            status_db_gateway: IStatusDBGateway,
            recruitment_db_gateway: IRecruitmentDBGateway,
            ulid_generator: ULIDGenerator,
            db_session: DBSession,
            candidate_service: CandidateService,
            user_service: UserService,
            status_service: StatusService,
            minio: IMinIOClient,
            config: ApplicationConfig,
            template: ITemplate,
    ) -> None:
        self.candidate_db_gateway = candidate_db_gateway
        self.candidate_yandex_form_db_gateway=candidate_yandex_form_db_gateway
        self.candidate_form_db_gateway = candidate_form_db_gateway
        self.candidate_approval_db_gateway = candidate_approval_db_gateway
        self.candidate_statement_db_gateway = candidate_statement_db_gateway
        self.broker = broker
        self.user_db_gateway = user_db_gateway
        self.status_db_gateway = status_db_gateway
        self.recruitment_db_gateway = recruitment_db_gateway
        self.ulid_generator = ulid_generator
        self.db_session = db_session
        self.candidate_service = candidate_service
        self.user_service = user_service
        self.role_db_gateway = role_db_gateway
        self.status_service = status_service
        self.minio = minio
        self.config = config
        self.template = template

    async def add(self, request: AddCandidateDTO) -> GetCandidateDTO:
        if request.telegram_id:
            role = await self.role_db_gateway.get_role(name=RoleEnum.CANDIDATE)
            user = self.user_service.add_user(
                **asdict(request),
                id=str(self.ulid_generator()),
                role_id=role.id,
            )
            await self.user_db_gateway.insert(user)
        candidate = self.candidate_service.add_candidate(
            **asdict(request),
            id=str(self.ulid_generator()),
        )
        candidate = await self.candidate_db_gateway.insert(candidate)
        status = self.status_service.add_status(
            id=str(self.ulid_generator()),
            candidate_id=candidate.id,
        )
        await self.status_db_gateway.insert(status)
        data = self.candidate_service.get_candidate(candidate=candidate)
        await self._save_documents(data.copy())
        await self.db_session.commit()
        return GetCandidateDTO(**data)

    async def get_candidate_document(
            self,
            request: CandidateDocumentNameDTO,
    ) -> GetDocumentDTO:
        gateways = {
            "form": self.candidate_form_db_gateway,
            "approval": self.candidate_approval_db_gateway,
            "statement": self.candidate_statement_db_gateway,
        }
        gateway = gateways.get(request.name)
        document = await gateway.get(
            candidate_id=request.id or request.telegram_id,
        )
        data = self.candidate_service.get_document(document)
        return GetDocumentDTO(**data)

    async def add_or_update_approval(
            self,
            request: UpdateDocumentDTO,
    ) -> GetDocumentDTO:
        document = await self.candidate_approval_db_gateway.get(
            candidate_id=request.candidate_id,
        )
        if document is None:
            return await self._add_document(
                request=request,
                bucket=self.config.s3.candidate_bucket,
                db_gateway="candidate_approval_db_gateway",
            )
        return await self._update_document(
            request=request,
            document=document,
            bucket=self.config.s3.candidate_bucket,
            db_gateway="candidate_approval_db_gateway",
        )

    async def add_or_update_statement(
            self,
            request: UpdateDocumentDTO,
    ) -> GetDocumentDTO:
        document = await self.candidate_statement_db_gateway.get(
            candidate_id=request.candidate_id,
        )
        if document is None:
            return await self._add_document(
                request=request,
                bucket=self.config.s3.candidate_bucket,
                db_gateway="candidate_statement_db_gateway",
            )
        return await self._update_document(
            request=request,
            document=document,
            bucket=self.config.s3.candidate_bucket,
            db_gateway="candidate_statement_db_gateway",
        )

    async def add_or_update_form(
            self,
            request: UpdateDocumentDTO,
    ) -> GetDocumentDTO:
        document = await self.candidate_form_db_gateway.get(
            candidate_id=request.candidate_id,
        )
        if document is None:
            return await self._add_document(
                request,
                bucket=self.config.s3.candidate_bucket,
                db_gateway="candidate_form_db_gateway",
            )
        return await self._update_document(
            request,
            document,
            bucket=self.config.s3.candidate_bucket,
            db_gateway="candidate_form_db_gateway",
        )

    async def get(self, request: AddCandidateIDDTO) -> GetCandidateDTO:
        candidate = await self.candidate_db_gateway.get(
            candidate_id=request.id,
            telegram_id=request.telegram_id,
        )
        data = self.candidate_service.get_candidate(
            candidate=candidate,
        )
        return GetCandidateDTO(**data)

    async def update(self, request: UpdateCandidateDTO) -> GetCandidateDTO:
        candidate = await self.candidate_db_gateway.get(
            candidate_id=request.id,
            telegram_id=request.telegram_id,
        )
        # TODO: добавить taskiq и отдельную задачу
        context = self.candidate_service.get_candidate(candidate)
        candidate = self.candidate_service.update_candidate(
            candidate=candidate,
            **asdict(request),
        )
        await self.candidate_db_gateway.update(candidate=candidate)
        data = self.candidate_service.get_candidate(candidate)
        # TODO: добавить taskiq и отдельную задачу
        await self._delete_form(
            context=context,
        )
        await self._save_documents_full(data.copy())
        await self.db_session.commit()
        return GetCandidateDTO(**data)

    async def all(self, request: PaginationDTO) -> GetCandidatesDTO:
        candidates = self.candidate_db_gateway.all(
            limit=request.limit,
            offset=request.offset * request.limit,
        )
        result = []
        async for candidate in candidates:
            data = self.candidate_service.get_candidate(candidate)
            result.append(GetCandidateDTO(**data))
        total = await self.candidate_db_gateway.get_total()
        return GetCandidatesDTO(
            total=total,
            limit=request.limit,
            offset=request.offset,
            values=result,
        )

    async def get_by_recruitment_id(self, recruitment_id: str, limit: int, offset: int):
        candidates = await self.candidate_db_gateway.get_by_recruitment_id(recruitment_id=recruitment_id, limit=limit, offset=offset)
        all_candidates = await self.candidate_db_gateway.get_by_recruitment_id_all(recruitment_id=recruitment_id)

        result = []
        for c in candidates:
            result.append({
                "id": c.id,
                "telegram_id": c.telegram_id,
                "first_name": c.first_name,
                "is_approval": c.is_approval,
            })
        result.append({"total": len(all_candidates)})
        return result

    async def _delete_form(self, context: dict[str, Any]) -> None:
        document = await self.candidate_form_db_gateway.get(
            candidate_id=context.get("id"),
        )
        path = (
            document
            .url
            .replace(f"{self.config.s3.endpoint}/", "")
            .replace(f"{self.config.template.candidate_bucket}/", "")
        )
        await self.minio.delete_object(
            bucket=self.config.template.candidate_bucket,
            key=path,
        )

    async def _delete_candidate_files(self, context: dict[str, Any]) -> None:
        candidate_form = await self.candidate_form_db_gateway.get(
            candidate_id=context.get("id"),
        )
        candidate_approval = await self.candidate_approval_db_gateway.get(
            candidate_id=context.get("id"),
        )
        candidate_statement = await self.candidate_statement_db_gateway.get(
            candidate_id=context.get("id"),
        )
        
        if candidate_form:
            path_form = (candidate_form.url.replace(f"{self.config.s3.endpoint}/", "")
                    .replace(f"{self.config.template.candidate_bucket}/", "")
            )
            await self.minio.delete_object(
                bucket=self.config.template.candidate_bucket,
                key=path_form,
            )
        if candidate_approval:
            path_approval = (candidate_approval.url.replace(f"{self.config.s3.endpoint}/", "")
                    .replace(f"{self.config.template.candidate_bucket}/", "")
            )
            await self.minio.delete_object(
                bucket=self.config.template.candidate_bucket,
                key=path_approval,
            )
        if candidate_statement:
            path_statement = (candidate_statement.url.replace(f"{self.config.s3.endpoint}/", "")
                .replace(f"{self.config.template.candidate_bucket}/", "")
            )
            await self.minio.delete_object(
                bucket=self.config.template.candidate_bucket,
                key=path_statement,
            )


    async def _save_documents(self, context: dict[str, Any]) -> None:
        buffer = io.BytesIO()
        async for val in self.minio.get_object(
                bucket=self.config.template.candidate_bucket,
                key=self.config.template.candidate_name_template,
        ):
            buffer.write(val)
        file = await self.template.get_docx(
            template=buffer,
            context=context,
        )
        recruitment = await self.recruitment_db_gateway.get(
            recruitment_id=context.get("recruitment_id"),
        )
        path_form = self.candidate_service.get_path_document(
            name="Лист собеседования.docx",
            recruitment=recruitment.name,
            **context,
        )
        tasks = [
            self.candidate_approval_db_gateway.get(
                context.get("id"),
            ),
            self.candidate_statement_db_gateway.get(
                context.get("id"),
            ),
        ]
        result = await asyncio.gather(*tasks)
        models = await self._load_task_documents(result)
        await self.minio.put_object(
            bucket=self.config.template.candidate_bucket,
            key=path_form,
            file=file,
        )
        await self._move_object(
            context=context | {
                "recruitment": recruitment.name,
            },
            models=models,
        )
        await self._save_form_url(
            context=context,
            url=f"{self.config.s3.endpoint}/"
                f"{self.config.template.candidate_bucket}/{path_form}",
        )


    async def _save_documents_full(self, context: dict[str, Any]) -> None:
        buffer = io.BytesIO()
        async for val in self.minio.get_object(
                bucket=self.config.template.candidate_bucket,
                key=self.config.template.candidate_name_template_full,
        ):
            buffer.write(val)
        file = await self.template.get_docx(
            template=buffer,
            context=context,
        )
        recruitment = await self.recruitment_db_gateway.get(
            recruitment_id=context.get("recruitment_id"),
        )
        path_form = self.candidate_service.get_path_document(
            name="Лист собеседования.docx",
            recruitment=recruitment.name,
            **context,
        )
        tasks = [
            self.candidate_approval_db_gateway.get(
                context.get("id"),
            ),
            self.candidate_statement_db_gateway.get(
                context.get("id"),
            ),
        ]
        result = await asyncio.gather(*tasks)
        models = await self._load_task_documents(result)
        await self.minio.put_object(
            bucket=self.config.template.candidate_bucket,
            key=path_form,
            file=file,
        )
        await self._move_object(
            context=context | {
                "recruitment": recruitment.name,
            },
            models=models,
        )
        await self._save_form_url(
            context=context,
            url=f"{self.config.s3.endpoint}/"
                f"{self.config.template.candidate_bucket}/{path_form}",
        )

    async def _move_object(self,
            context: dict[str, Any],
            models: dict[str, CandidateDocument],
    ) -> None:
        gateways = {
            "approval": self.candidate_approval_db_gateway,
            "statement": self.candidate_statement_db_gateway,
        }
        for key, value in models.items():
            if value is None:
                continue
            gateway = gateways.get(key)
            data = self.candidate_service.get_document(document=value)
            path = self.candidate_service.get_path(
                endpoint=self.config.s3.endpoint,
                url=data.get("url"),
                bucket_name=self.config.s3.candidate_bucket,
            )
            name = data.get("name")
            new_path = self.candidate_service.get_path_document(
                name=name,
                **context,
            )
            await self.minio.copy_object(
                bucket=self.config.s3.candidate_bucket,
                old_key=path,
                new_key=new_path,
            )
            if path != new_path:
                await self.minio.delete_object(
                    bucket=self.config.s3.candidate_bucket,
                    key=path,
                )
            new_document = self.candidate_service.update_document(
                document=value,
                url=self.candidate_service.get_url(
                    endpoint=self.config.s3.endpoint,
                    bucket=self.config.s3.candidate_bucket,
                    path=new_path,
                ),
            )
            await gateway.update(new_document)

    async def _load_task_documents(
            self,
            tasks: list[Any],
    ) -> dict[str, CandidateDocument]:
        approval_document, statement_document = tasks
        return {
            "approval": approval_document,
            "statement": statement_document,
        }

    async def _save_form_url(self, context: dict[str, Any], url: str) -> None:
        name = url.split("/")[-1]
        document = await self.candidate_form_db_gateway.get(
            candidate_id=context.get("id"),
        )
        if not document:
            document = self.candidate_service.add_document(
                id=str(self.ulid_generator()),
                name=name,
                url=url,
                candidate_id=context.get("id"),
            )
            await self.candidate_form_db_gateway.insert(document)
            return
        # TODO: переделать
        document = self.candidate_service.update_document(
            document=document,
            id=str(self.ulid_generator()),
            name=name,
            url=url,
            candidate_id=context.get("id"),
        )
        await self.candidate_form_db_gateway.update(document)

    async def _add_document(
            self,
            request: UpdateDocumentDTO,
            bucket: str,
            db_gateway: str,
    ) -> GetDocumentDTO:
        candidate = await self.candidate_db_gateway.get(
            candidate_id=request.candidate_id,
            telegram_id=request.candidate_id,
        )
        data = self.candidate_service.get_candidate(candidate=candidate)
        recruitment = await self.recruitment_db_gateway.get(
            recruitment_id=data.get("recruitment_id"),
        )
        path = self.candidate_service.get_path_document(
            name=request.filename,
            recruitment=recruitment.name,
            **data,
        )
        await self.minio.put_object(
            bucket=bucket,
            key=path,
            file=self.candidate_service.get_file(file=request.file),
        )
        url = self.candidate_service.get_url(
            endpoint=self.config.s3.endpoint,
            bucket=bucket,
            path=path,
        )
        document = self.candidate_service.add_document(
            id=str(self.ulid_generator()),
            name=url.split("/")[-1],
            url=url,
            candidate_id=data.get("id"),
        )
        method = getattr(self, db_gateway)
        await method.insert(document)
        await self.db_session.commit()
        data = self.candidate_service.get_document(document)
        return GetDocumentDTO(**data)

    async def _update_document(self,
            request: UpdateDocumentDTO,
            document: CandidateDocument,
            bucket: str,
            db_gateway: str,
    ) -> GetDocumentDTO:
        data = self.candidate_service.get_document(document)
        path = self.candidate_service.get_path(
            endpoint=self.config.s3.endpoint,
            url=data.get("url"),
            bucket_name=bucket,
        )
        new_path = self.candidate_service.update_path(
            path=path,
            filename=request.filename,
        )
        document = self.candidate_service.update_document(
            document=document,
            name=request.filename,
            url=f"{self.config.s3.endpoint}/"
                f"{bucket}/{new_path}",
            candidate_id=request.candidate_id,
        )
        method = getattr(self, db_gateway)
        await method.update(document=document)
        await self.minio.delete_object(
            bucket=bucket,
            key=path,
        )
        await self.minio.put_object(
            bucket=bucket,
            key=new_path,
            file=self.candidate_service.get_file(file=request.file),
        )
        data = self.candidate_service.get_document(document)
        await self.db_session.commit()
        return GetDocumentDTO(**data)


    async def delete_candidate(self, candidate_id: str, telegram_id: str):
        await self._delete_candidate_files(context={"id": candidate_id})
        await self.candidate_approval_db_gateway.delete(candidate_id)
        await self.candidate_form_db_gateway.delete(candidate_id)
        await self.candidate_statement_db_gateway.delete(candidate_id)
        await self.status_db_gateway.delete(candidate_id)
        await self.candidate_db_gateway.delete(candidate_id)

        await self.broker.publish(
            message={
                "telegram_id": telegram_id,
            },
            queue="delete_candidate_for_soc",
        )

        await self.db_session.commit()


    async def update_for_form(self, request: FormDataDTO):
        candidate = await self.candidate_db_gateway.get(
            candidate_id=request.candidate_id,
            telegram_id=request.telegram_id,
        )
        context = self.candidate_service.get_candidate(candidate)      #составляем словарь из данных кандидата
        candidate = self.candidate_service.update_candidate(           #обновляем модель кандидата из новых данных
            candidate=candidate,
            **asdict(request),
        )
        candidate_dict = self.candidate_service.update_candidate_from_form(     #тут словарь вернулся с полными данными и кандидатскими данными
            candidate=candidate,
            **asdict(request),
        )

        await self.broker.publish(
            candidate_dict,
            queue="candidate_new_yandex_form",
        )
        
        await self.candidate_db_gateway.update(candidate=candidate) 
        await self._delete_form(context=context,)
        await self._save_documents_full(candidate_dict.copy())
        await self.db_session.commit()
        
        return candidate_dict
    

    async def add_candidate_from_form(self, request: FormDataDTO):
        candidate_form_db = await self.candidate_yandex_form_db_gateway.get(
            telegram_id=request.telegram_id
        )
        if candidate_form_db == None:
            candidate_form = self.candidate_service.add_candidate_data_from_form(
                **asdict(request),
                id=str(self.ulid_generator()),
            )
            candidate_form = await self.candidate_yandex_form_db_gateway.insert(candidate_form=candidate_form) 
        
        else:
            new_candidate_form = self.candidate_service.update_candidate_form(    
                candidate_form=candidate_form_db,
                **asdict(request),
            )
            candidate_form = await self.candidate_yandex_form_db_gateway.update(candidate_form=new_candidate_form) 

        await self.db_session.commit()
        return candidate_form

