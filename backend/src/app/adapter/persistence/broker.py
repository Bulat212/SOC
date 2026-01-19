from faststream.rabbit import RabbitBroker

from app.config import BrokerConfig


def new_broker(config: BrokerConfig) -> RabbitBroker:
    return RabbitBroker(config.url)
