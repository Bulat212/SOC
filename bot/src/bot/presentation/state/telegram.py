from aiogram.fsm.state import StatesGroup, State


class TelegramChannelState(StatesGroup):
    telegram_channel_url = State()
