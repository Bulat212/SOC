from collections.abc import AsyncIterable

import ulid
from aiobotocore.session import get_session as get_session_s3
from dishka import Provider, Scope, from_context, provide, AnyOf
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from types_aiobotocore_s3.client import S3Client
from faststream.rabbit import RabbitBroker

from app.adapter.db.gateway.answer import AnswerDBGateway
from app.adapter.db.gateway.candidate import (
    CandidateDBGateway,
    CandidateFormDBGateway,
    CandidateApprovalDBGateway,
    CandidateStatementDBGateway,
    CandidateYandexFormGateway,
)
from app.adapter.db.gateway.document import (
    PromoDocumentDBGateway,
    DocumentDBGateway,
)
from app.adapter.db.gateway.faq import FaqDBGateway
from app.adapter.db.gateway.info import InfoDBGateway
from app.adapter.db.gateway.question import QuestionDBGateway
from app.adapter.db.gateway.recruitment import RecruitmentDBGateway
from app.adapter.db.gateway.role import RoleDBGateway
from app.adapter.db.gateway.status import StatusDBGateway
from app.adapter.db.gateway.user import UserDBGateway
from app.adapter.document.template import Template
from app.adapter.db.gateway.delegate import DelegateDBGateway
from app.adapter.persistence.db import new_session_maker
from app.adapter.s3.minio import MinIOClient
from app.application.interface.db import DBSession
from app.application.interface.document.template import ITemplate
from app.application.interface.gateway.answer import IAnswerDBGateway
from app.application.interface.gateway.candidate import (
    ICandidateDBGateway,
    ICandidateFormDBGateway,
    ICandidateApprovalDBGateway,
    ICandidateStatementDBGateway,
    ICandidateYandexFormGateway,
)
from app.application.interface.gateway.document import (
    IPromoDocumentDBGateway,
    IDocumentDBGateway,
)
from app.application.interface.gateway.delegate import IDelegateDBGateway
from app.application.interface.gateway.faq import IFaqDBGateway
from app.application.interface.gateway.info import IInfoDBGateway
from app.application.interface.gateway.question import IQuestionDBGateway
from app.application.interface.gateway.recruitment import IRecruitmentDBGateway
from app.application.interface.gateway.role import IRoleDBGateway
from app.application.interface.gateway.status import IStatusDBGateway
from app.application.interface.gateway.user import IUserDBGateway
from app.application.interface.s3.client import IMinIOClient
from app.application.interface.ulid_generator import ULIDGenerator
from app.application.usecase.answer import AnswerUseCase
from app.application.usecase.candidate import CandidateUseCase
from app.application.usecase.document import (
    PromoDocumentUseCase,
    DocumentUseCase,
)
from app.application.usecase.faq import FaqUseCase
from app.application.usecase.info import InfoUseCase
from app.application.usecase.question import QuestionUseCase
from app.application.usecase.recruitment import RecruitmentUseCase
from app.application.usecase.status import StatusUseCase
from app.application.usecase.user import UserUseCase
from app.application.usecase.delegate import DelegateUseCase
from app.config import ApplicationConfig
from app.domain.service.answer import AnswerService
from app.domain.service.candidate import CandidateService
from app.domain.service.document import PromoDocumentService, DocumentService
from app.domain.service.faq import FaqService
from app.domain.service.info import InfoService
from app.domain.service.question import QuestionService
from app.domain.service.recruitment import RecruitmentService
from app.domain.service.role import RoleService
from app.domain.service.status import StatusService
from app.domain.service.user import UserService
from app.domain.service.delegate import DelegateService


class BaseProvider(Provider):
    config = from_context(provides=ApplicationConfig, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_ulid_generator(self) -> ULIDGenerator:
        return ulid.ULID

    @provide(scope=Scope.APP)
    def get_session_maker(
            self,
            config: ApplicationConfig,
    ) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config=config.database)

    @provide(scope=Scope.REQUEST)
    async def get_session(
            self,
            session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AnyOf[AsyncSession, DBSession]]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    async def get_client_s3(
            self,
            config: ApplicationConfig,
    ) -> AsyncIterable[S3Client]:
        s3_config = config.s3
        async with get_session_s3().create_client(
                "s3",
                endpoint_url=s3_config.endpoint,
                aws_access_key_id=s3_config.access_key,
                aws_secret_access_key=s3_config.secret_key,
                verify=s3_config.verify,
        ) as client:
            yield client

    @provide(scope=Scope.REQUEST)
    async def get_minio_client(
            self,
            client: S3Client,
    ) -> AnyOf[MinIOClient, IMinIOClient]:
        return MinIOClient(
            client=client,
        )

    @provide(scope=Scope.REQUEST)
    async def get_template(self) -> AnyOf[Template, ITemplate]:
        return Template()
    
    @provide(scope=Scope.APP)
    async def get_broker(
        self,
        config: ApplicationConfig,  
    ) -> AsyncIterable[RabbitBroker]:
        broker = RabbitBroker(config.broker.url)
        async with broker:
            yield broker


class UserProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_user_usecase(
            self,
            user_gateway: IUserDBGateway,
            role_gateway: IRoleDBGateway,
            ulid_generator: ULIDGenerator,
            db_session: DBSession,
    ) -> UserUseCase:
        return UserUseCase(
            user_gateway=user_gateway,
            role_gateway=role_gateway,
            ulid_generator=ulid_generator,
            db_session=db_session,
            user_service=UserService(),
            role_service=RoleService(),
        )

    user_db_gateway = provide(
        UserDBGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[UserDBGateway, IUserDBGateway],
    )


class DelegateProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_delegate_usecase(
            self,
            delegate_gateway: IDelegateDBGateway,
            db_session: DBSession,
            role_db_gateway: IRoleDBGateway,
            ulid_generator: ULIDGenerator,

    ) -> DelegateUseCase:
        return DelegateUseCase(
            delegate_gateway=delegate_gateway,
            db_session=db_session,
            delegate_service=DelegateService(),
            ulid_generator=ulid_generator,
            role_db_gateway=role_db_gateway,
        )
    
    delegate_db_gateway = provide(
        DelegateDBGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[DelegateDBGateway, IDelegateDBGateway],
    )


class RoleProvider(Provider):
    # Gateway
    role_db_gateway = provide(
        RoleDBGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[RoleDBGateway, IRoleDBGateway],
    )


class RecruitmentProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_recruitment_usecase(
            self,
            recruitment_gateway: IRecruitmentDBGateway,
    ) -> RecruitmentUseCase:
        return RecruitmentUseCase(
            recruitment_gateway=recruitment_gateway,
            recruitment_service=RecruitmentService(),
        )

    recruitment_db_gateway = provide(
        RecruitmentDBGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[RecruitmentDBGateway, IRecruitmentDBGateway],
    )


class CandidateProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_candidates_usecase(
            self,
            candidate_db_gateway: ICandidateDBGateway,
            candidate_yandex_form_db_gateway: ICandidateYandexFormGateway,
            candidate_document_db_gateway: ICandidateFormDBGateway,
            candidate_approval_db_gateway: ICandidateApprovalDBGateway,
            candidate_statement_db_gateway: ICandidateStatementDBGateway,
            user_db_gateway: IUserDBGateway,
            role_db_gateway: IRoleDBGateway,
            status_db_gateway: IStatusDBGateway,
            recruitment_db_gateway: IRecruitmentDBGateway,
            ulid_generator: ULIDGenerator,
            db_session: DBSession,
            minio: IMinIOClient,
            config: ApplicationConfig,
            template: ITemplate,
            broker: RabbitBroker,
    ) -> CandidateUseCase:
        return CandidateUseCase(
            candidate_db_gateway=candidate_db_gateway,
            candidate_yandex_form_db_gateway=candidate_yandex_form_db_gateway,
            candidate_form_db_gateway=candidate_document_db_gateway,
            candidate_approval_db_gateway=candidate_approval_db_gateway,
            candidate_statement_db_gateway=candidate_statement_db_gateway,
            user_db_gateway=user_db_gateway,
            ulid_generator=ulid_generator,
            recruitment_db_gateway=recruitment_db_gateway,
            db_session=db_session,
            candidate_service=CandidateService(),
            user_service=UserService(),
            role_db_gateway=role_db_gateway,
            status_db_gateway=status_db_gateway,
            status_service=StatusService(),
            minio=minio,
            config=config,
            template=template,
            broker=broker,
        )

    candidate_db_gateway = provide(
        CandidateDBGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[CandidateDBGateway, ICandidateDBGateway],
    )
    candidate_yandex_form_db_gateway = provide(
        CandidateYandexFormGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[CandidateYandexFormGateway, ICandidateYandexFormGateway],
    )
    candidate_document_db_gateway = provide(
        CandidateFormDBGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[
            CandidateFormDBGateway,
            ICandidateFormDBGateway,
        ],
    )
    candidate_approval_db_gateway = provide(
        CandidateApprovalDBGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[
            CandidateApprovalDBGateway,
            ICandidateApprovalDBGateway,
        ],
    )
    candidate_statement_db_gateway = provide(
        CandidateStatementDBGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[
            CandidateStatementDBGateway,
            ICandidateStatementDBGateway,
        ],
    )


class InfoProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_info_usecase(
            self,
            info_db_gateway: IInfoDBGateway,
    ) -> InfoUseCase:
        return InfoUseCase(
            info_db_gateway=info_db_gateway,
            info_service=InfoService(),
        )

    # Gateway
    info_db_gateway = provide(
        InfoDBGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[InfoDBGateway, IInfoDBGateway],
    )


class StatusProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_status_usecase(
            self,
            status_db_gateway: IStatusDBGateway,
            candidate_db_gateway: ICandidateDBGateway,
    ) -> StatusUseCase:
        return StatusUseCase(
            status_db_gateway=status_db_gateway,
            candidate_db_gateway=candidate_db_gateway,
            candidate_service=CandidateService(),
            status_service=StatusService(),
        )

    status_db_gateway = provide(
        StatusDBGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[StatusDBGateway, IStatusDBGateway],
    )


class PromoDocumentProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_promo_document_usecase(
            self,
            promo_document_db_gateway: IPromoDocumentDBGateway,
            info_db_gateway: IInfoDBGateway,
            ulid_genearator: ULIDGenerator,
            minio: IMinIOClient,
            config: ApplicationConfig,
            db_session: DBSession,
    ) -> PromoDocumentUseCase:
        return PromoDocumentUseCase(
            promo_document_db_gateway=promo_document_db_gateway,
            info_db_gateway=info_db_gateway,
            info_service=InfoService(),
            promo_document_service=PromoDocumentService(),
            ulid_generator=ulid_genearator,
            minio=minio,
            config=config,
            db_session=db_session,
        )

    promo_document_db_gateway = provide(
        PromoDocumentDBGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[PromoDocumentDBGateway, IPromoDocumentDBGateway],
    )


class DocumentProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_document_usecase(
            self,
            document_db_gateway: IDocumentDBGateway,
            info_db_gateway: IInfoDBGateway,
    ) -> DocumentUseCase:
        return DocumentUseCase(
            document_db_gateway=document_db_gateway,
            info_db_gateway=info_db_gateway,
            info_service=InfoService(),
            document_service=DocumentService(),
        )

    document_db_gateway = provide(
        DocumentDBGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[DocumentDBGateway, IDocumentDBGateway],
    )


class FaqProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_faq_usecase(
            self,
            faq_db_gateway: IFaqDBGateway,
            ulid_generator: ULIDGenerator,
            db_session: DBSession,
    ) -> FaqUseCase:
        return FaqUseCase(
            faq_db_gateway=faq_db_gateway,
            faq_service=FaqService(),
            ulid_generator=ulid_generator,
            db_session=db_session,
        )

    faq_db_gateway = provide(
        FaqDBGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[FaqDBGateway, IFaqDBGateway],
    )


class QuestionProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_question_usecase(
            self,
            question_db_gateway: IQuestionDBGateway,
            user_db_gateway: IUserDBGateway,
            db_session: DBSession,
            ulid_generator: ULIDGenerator,
    ) -> QuestionUseCase:
        return QuestionUseCase(
            question_db_gateway=question_db_gateway,
            user_db_gateway=user_db_gateway,
            db_session=db_session,
            user_service=UserService(),
            question_service=QuestionService(),
            ulid_generator=ulid_generator,
        )

    question_db_gateway = provide(
        QuestionDBGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[QuestionDBGateway, IQuestionDBGateway],
    )


class AnswerProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_answer_usecase(
            self,
            answer_db_gateway: IAnswerDBGateway,
            question_db_gateway: IQuestionDBGateway,
            ulid_generator: ULIDGenerator,
            db_session: DBSession,
    ) -> AnswerUseCase:
        return AnswerUseCase(
            answer_db_gateway=answer_db_gateway,
            question_db_gateway=question_db_gateway,
            ulid_generator=ulid_generator,
            db_session=db_session,
            service=AnswerService(),
        )

    answer_db_gateway = provide(
        AnswerDBGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[AnswerDBGateway, IAnswerDBGateway],
    )
