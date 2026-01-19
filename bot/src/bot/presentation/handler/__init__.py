from .document_router import document_router
from .hello_router import hello_router
from .info_router import info_router
from .my_data_router import my_data_router
from .promo_router import promo_router
from .question_router import question_router
from .status_router import status_router
from .telegram_router import telegram_router
from .faq_router import faq_router
from .add_candidate_router import add_candidate_router
from .get_candidate_router import get_candidate_router
from .delete_candidate_router import delete_candidate_router

__all__ = (
    "hello_router",
    "my_data_router",
    "status_router",
    "telegram_router",
    "promo_router",
    "document_router",
    "question_router",
    "info_router",
    "faq_router",
    "add_candidate_router",
    "get_candidate_router",
    "delete_candidate_router",
)
