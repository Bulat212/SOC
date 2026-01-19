from dishka.integrations.faststream import FromDishka, inject
from faststream.nats import NatsRouter

from app.application.interactor.telegram import GetTelegramChannelInteractor
from app.presentation.schema.telegram import GetTelegramChannelSchema

telegram_router = NatsRouter()


@telegram_router.subscriber(
    subject="get_telegram_channel",
    queue="telegram",
)
@inject
async def get_telegram_channel(
    interactor: FromDishka[GetTelegramChannelInteractor],
) -> GetTelegramChannelSchema:
    result = await interactor()
    return GetTelegramChannelSchema(
        channel=result.channel,
    )
