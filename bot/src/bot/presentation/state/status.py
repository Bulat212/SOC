from aiogram.fsm.state import StatesGroup, State


class StatusState(StatesGroup):
    status = State()
