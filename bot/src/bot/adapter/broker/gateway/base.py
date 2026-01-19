from faststream.rabbit import RabbitBroker


class BaseBrokerGateway:
    def __init__(self, broker: RabbitBroker) -> None:
        self.broker = broker
