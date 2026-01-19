from collections.abc import AsyncIterable

from faststream.rabbit import RabbitBroker

from bot.config import BrokerConfig


async def new_broker(config: BrokerConfig) -> AsyncIterable[RabbitBroker]:
    broker = RabbitBroker(config.url)
    async with broker as session:
        yield session
