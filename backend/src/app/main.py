from dishka import make_async_container
from dishka.integrations import faststream as faststream_integration
from faststream import FastStream

from app.adapter.persistence.broker import new_broker
from app.config import ApplicationConfig, load_config
from app.ioc import (
    UserProvider,
    RecruitmentProvider,
    CandidateProvider,
    BaseProvider,
    RoleProvider,
    InfoProvider,
    StatusProvider,
    PromoDocumentProvider,
    DocumentProvider,
    FaqProvider,
    QuestionProvider,
    AnswerProvider,
    DelegateProvider,
)
from app.presentation.broker.answer import answer_router
from app.presentation.broker.candidate import candidate_router
from app.presentation.broker.document import document_router
from app.presentation.broker.faq import faq_router
from app.presentation.broker.info import info_router
from app.presentation.broker.question import question_router
from app.presentation.broker.recruitment import recruitment_router
from app.presentation.broker.status import status_router
from app.presentation.broker.user import user_router
from app.presentation.broker.delegate import delegate_router

config = load_config()
container = make_async_container(
    BaseProvider(),
    RoleProvider(),
    UserProvider(),
    InfoProvider(),
    StatusProvider(),
    RecruitmentProvider(),
    CandidateProvider(),
    PromoDocumentProvider(),
    DocumentProvider(),
    FaqProvider(),
    QuestionProvider(),
    AnswerProvider(),
    DelegateProvider(),
    context={
        ApplicationConfig: config,
    },
)


def get_faststream_app() -> FastStream:
    broker = new_broker(config.broker)
    app = FastStream(broker)
    faststream_integration.setup_dishka(container, app, auto_inject=True)
    broker.include_routers(
        user_router,
        recruitment_router,
        candidate_router,
        info_router,
        status_router,
        document_router,
        faq_router,
        question_router,
        answer_router,
        delegate_router,
    )
    return app
