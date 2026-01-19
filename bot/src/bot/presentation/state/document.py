from aiogram.fsm.state import StatesGroup, State


class DocumentState(StatesGroup):
    start_guarding = State()
    start = State()
    invalid = State()
