from aiogram.fsm.state import StatesGroup, State


class InfoState(StatesGroup):
    start = State()
    back = State()
