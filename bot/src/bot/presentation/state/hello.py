from aiogram.fsm.state import StatesGroup, State


class HelloState(StatesGroup):
    active = State()
    not_active = State()
