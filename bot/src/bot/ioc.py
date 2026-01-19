from collections.abc import AsyncIterable

from dishka import Provider, Scope, from_context, provide, AnyOf
from faststream.rabbit import RabbitBroker

from bot.adapter.broker.gateway.answer import AnswerBrokerGateway
from bot.adapter.broker.gateway.candidate import CandidateBrokerGateway
from bot.adapter.broker.gateway.document import DocumentBrokerGateway
from bot.adapter.broker.gateway.faq import FaqBrokerGateway
from bot.adapter.broker.gateway.info import InfoBrokerGateway
from bot.adapter.broker.gateway.promo import PromoBrokerGateway
from bot.adapter.broker.gateway.question import QuestionBrokerGateway
from bot.adapter.broker.gateway.recruitment import RecruitmentBrokerGateway
from bot.adapter.broker.gateway.status import StatusBrokerGateway
from bot.adapter.broker.gateway.user import UserBrokerGateway
from bot.adapter.broker.gateway.delegate import DelegateBrokerGateway

from bot.application.interface.broker.gateway.answer import (
    IAnswerBrokerGateway,
)
from bot.application.interface.broker.gateway.candidate import (
    ICandidateBrokerGateway,
)
from bot.application.interface.broker.gateway.document import (
    IDocumentBrokerGateway,
)
from bot.application.interface.broker.gateway.faq import IFaqBrokerGateway
from bot.application.interface.broker.gateway.info import IInfoBrokerGateway
from bot.application.interface.broker.gateway.promo import IPromoBrokerGateway
from bot.application.interface.broker.gateway.question import (
    IQuestionBrokerGateway,
)
from bot.application.interface.broker.gateway.recruitment import (
    IRecruitmentBrokerGateway,
)
from bot.application.interface.broker.gateway.status import (
    IStatusBrokerGateway,
)
from bot.application.interface.broker.gateway.user import IUserBrokerGateway
from bot.application.interface.broker.gateway.delegate import IDelegateBrokerGateway
from bot.application.usecase.answer import AnswerUseCase
from bot.application.usecase.candidate import CandidateUseCase
from bot.application.usecase.document import DocumentUseCase
from bot.application.usecase.faq import FaqUseCase
from bot.application.usecase.info import InfoUseCase
from bot.application.usecase.promo import PromoUseCase
from bot.application.usecase.question import QuestionUseCase
from bot.application.usecase.recruitment import RecruitmentUseCase
from bot.application.usecase.status import StatusUseCase
from bot.application.usecase.user import UserUseCase
from bot.application.usecase.delegate import DelegateUseCase
from bot.config import BotConfig
from bot.domain.service.answer import AnswerService
from bot.domain.service.candidate import CandidateService
from bot.domain.service.document import DocumentService
from bot.domain.service.faq import FaqService
from bot.domain.service.info import InfoService
from bot.domain.service.promo import PromoService
from bot.domain.service.question import QuestionService
from bot.domain.service.status import StatusService
from bot.domain.service.user import UserService
from bot.domain.service.delegate import DelegateService


class BaseProvider(Provider):
    config = from_context(provides=BotConfig, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_broker(
            self,
            config: BotConfig,
    ) -> AsyncIterable[RabbitBroker]:
        broker = RabbitBroker(
            config.broker.url,
        )
        async with broker as client:
            yield client


class UserProvider(BaseProvider):
    @provide(scope=Scope.REQUEST)
    def get_user_usecase(
            self,
            user_broker_gateway: IUserBrokerGateway,
    ) -> UserUseCase:
        return UserUseCase(
            user_broker_gateway=user_broker_gateway,
            user_service=UserService(),
        )

    # Broker gateway
    user_broker_gateway = provide(
        UserBrokerGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[UserBrokerGateway, IUserBrokerGateway],
    )


class DelegateProvider(BaseProvider):
    @provide(scope=Scope.REQUEST)
    def get_delegate_usecase(
        self,
        delegate_broker_gateway: IDelegateBrokerGateway
    ) -> DelegateUseCase:
        return DelegateUseCase(
            delegate_broker_gateway=delegate_broker_gateway,
            delegate_service=DelegateService(),
        )
    
    # Broker gateway
    delegate_broker_gateway = provide(
        DelegateBrokerGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[DelegateBrokerGateway, IDelegateBrokerGateway],
    )
    


class RecruitmentProvider(BaseProvider):
    @provide(scope=Scope.REQUEST)
    def get_recruitment_usecase(
            self,
            recruitment_broker_gateway: IRecruitmentBrokerGateway,
    ) -> RecruitmentUseCase:
        return RecruitmentUseCase(
            recruitment_broker_gateway=recruitment_broker_gateway,
        )

    # Broker gateway
    recruitment_broker_gateway = provide(
        RecruitmentBrokerGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[RecruitmentBrokerGateway, IRecruitmentBrokerGateway],
    )


class CandidateProvider(BaseProvider):
    @provide(scope=Scope.REQUEST)
    def get_candidate_usecase(
            self,
            candidate_broker_gateway: ICandidateBrokerGateway,
            recruitment_broker_gateway: IRecruitmentBrokerGateway,
    ) -> CandidateUseCase:
        return CandidateUseCase(
            candidate_broker_gateway=candidate_broker_gateway,
            recruitment_broker_gateway=recruitment_broker_gateway,
            candidate_service=CandidateService(),
            document_service=DocumentService(),
        )

    # Broker gateway
    candidate_broker_gateway = provide(
        CandidateBrokerGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[CandidateBrokerGateway, ICandidateBrokerGateway],
    )
    recruitment_broker_gateway = provide(
        RecruitmentBrokerGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[RecruitmentBrokerGateway, IRecruitmentBrokerGateway],
    )


class InfoProvider(BaseProvider):
    @provide(scope=Scope.REQUEST)
    def get_info_usecase(
            self,
            info_broker_gateway: IInfoBrokerGateway,
    ) -> InfoUseCase:
        return InfoUseCase(
            info_broker_gateway=info_broker_gateway,
            info_service=InfoService(),
        )

    # Broker gateway
    info_broker_gateway = provide(
        InfoBrokerGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[InfoBrokerGateway, IInfoBrokerGateway],
    )


class StatusProvider(BaseProvider):
    @provide(scope=Scope.REQUEST)
    def get_status_usecase(
            self,
            status_broker_gateway: IStatusBrokerGateway,
    ) -> StatusUseCase:
        return StatusUseCase(
            status_broker_gateway=status_broker_gateway,
            status_service=StatusService(),
        )

    status_broker_gateway = provide(
        StatusBrokerGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[StatusBrokerGateway, IStatusBrokerGateway],
    )


class PromoProvider(BaseProvider):
    @provide(scope=Scope.REQUEST)
    def get_promo_usecase(
            self,
            promo_broker_gateway: IPromoBrokerGateway,
    ) -> PromoUseCase:
        return PromoUseCase(
            promo_broker_gateway=promo_broker_gateway,
            promo_service=PromoService(),
        )

    promo_broker_gateway = provide(
        PromoBrokerGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[PromoBrokerGateway, IPromoBrokerGateway],
    )


class DocumentProvider(BaseProvider):
    @provide(scope=Scope.REQUEST)
    def get_document_usecase(
            self,
            document_broker_gateway: IDocumentBrokerGateway,
    ) -> DocumentUseCase:
        return DocumentUseCase(
            document_broker_gateway=document_broker_gateway,
            document_service=DocumentService(),
        )

    document_broker_gateway = provide(
        DocumentBrokerGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[DocumentBrokerGateway, IDocumentBrokerGateway],
    )


class FaqProvider(BaseProvider):
    @provide(scope=Scope.REQUEST)
    def get_faq_usecase(
            self,
            faq_broker_gateway: IFaqBrokerGateway,
    ) -> FaqUseCase:
        return FaqUseCase(
            faq_broker_gateway=faq_broker_gateway,
            faq_service=FaqService(),
        )

    faq_broker_gateway = provide(
        FaqBrokerGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[FaqBrokerGateway, IFaqBrokerGateway],
    )


class QuestionProvider(BaseProvider):
    @provide(scope=Scope.REQUEST)
    def get_question_usecase(
            self,
            question_broker_gateway: IQuestionBrokerGateway,
    ) -> QuestionUseCase:
        return QuestionUseCase(
            question_broker_gateway=question_broker_gateway,
            question_service=QuestionService(),
        )

    question_broker_gateway = provide(
        QuestionBrokerGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[QuestionBrokerGateway, IQuestionBrokerGateway],
    )


class AnswerProvider(BaseProvider):
    @provide(scope=Scope.REQUEST)
    def get_answer_usecase(
            self,
            answer_broker_gateway: IAnswerBrokerGateway,
    ) -> AnswerUseCase:
        return AnswerUseCase(
            answer_broker_gateway=answer_broker_gateway,
            answer_service=AnswerService(),
        )

    answer_broker_gateway = provide(
        AnswerBrokerGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[AnswerBrokerGateway, IAnswerBrokerGateway],
    )
