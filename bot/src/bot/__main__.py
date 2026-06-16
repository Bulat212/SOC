import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.enums import ParseMode
from aiogram.exceptions import AiogramError
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram_dialog import setup_dialogs
from dishka import make_async_container
from dishka.integrations.aiogram import setup_dishka
from redis.asyncio.client import Redis

from bot.config import BotConfig, load_config
from bot.ioc import (
    UserProvider,
    RecruitmentProvider,
    CandidateProvider,
    InfoProvider,
    StatusProvider,
    PromoProvider,
    DocumentProvider,
    FaqProvider,
    QuestionProvider,
    AnswerProvider,
    DelegateProvider,
)
from bot.presentation.dialog import (
    registration_dialog,
    about_us_dialog,
    my_data_dialog,
    status_dialog,
    telegram_dialog,
    promo_dialog,
    document_dialog,
    faq_dialog,
    my_document_dialog,
    question_dialog,
    answer_dialog,
    info_dialog,
    add_candidate_dialog,
    get_candidate_dialog,
    delete_candidate_dialog,
    delegate_data_dialog,
    delegate_dialog,
)
from bot.presentation.handler import (
    hello_router,
    my_data_router,
    status_router,
    telegram_router,
    promo_router,
    document_router,
    question_router,
    info_router,
    faq_router,
    add_candidate_router,
    get_candidate_router,
    delete_candidate_router,
)

logging.basicConfig(level=logging.DEBUG)


def include_routers(dp: Dispatcher):
    dp.include_routers(
        question_router,
        info_router,
        telegram_router,
        hello_router,
        my_data_router,
        status_router,
        promo_router,
        document_router,
        faq_router,
        add_candidate_router,
        get_candidate_router,
        delete_candidate_router,
        registration_dialog.dialog,
        about_us_dialog.dialog,
        my_data_dialog.dialog,
        status_dialog.dialog,
        telegram_dialog.dialog,
        promo_dialog.dialog,
        document_dialog.dialog,
        faq_dialog.dialog,
        my_document_dialog.dialog,
        question_dialog.dialog,
        answer_dialog.dialog,
        info_dialog.dialog,
        add_candidate_dialog.dialog,
        get_candidate_dialog.dialog,
        delete_candidate_dialog.dialog,
        delegate_data_dialog.dialog,
        delegate_dialog.dialog,
    )
import logging
logger = logging.getLogger(__name__)

async def start_bot(dp: Dispatcher, bot: Bot) -> None:
    try:
        await dp.start_polling(
            bot,
            skip_updates=True,
        )
    except AiogramError as e:
        logger.error(f"Polling failed: {e}", exc_info=True)
    finally:
        await bot.session.close()


def create_container(dp: Dispatcher, config: BotConfig) -> None:
    container = make_async_container(
        UserProvider(),
        RecruitmentProvider(),
        CandidateProvider(),
        InfoProvider(),
        StatusProvider(),
        PromoProvider(),
        DocumentProvider(),
        FaqProvider(),
        QuestionProvider(),
        AnswerProvider(),
        DelegateProvider(),
        context={BotConfig: config},
    )
    setup_dishka(
        container=container,
        router=dp,
        auto_inject=True,
    )


def get_storage(url: str) -> RedisStorage:
    storage = RedisStorage(
        redis=Redis.from_url(url),
        key_builder=DefaultKeyBuilder(with_destiny=True),
    )
    return storage


async def main() -> None:
    config = load_config()
    # logger.info(config.telegram_api_url)
    # print(config.telegram_api_url)
    # session = AiohttpSession(#83lKU17rGKnD
    #     api=TelegramAPIServer.from_base(
    #         config.telegram_api_url,
    #         is_local=True,
    #     ),
    # )
    session = AiohttpSession()  # без TelegramAPIServer
    bot = Bot(
        token=config.token,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(
        storage=get_storage(config.redis.url),
    )
    create_container(
        dp=dp,
        config=config,
    )
    setup_dialogs(dp)
    include_routers(dp)
    await start_bot(dp, bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
