from aiogram.fsm.state import StatesGroup, State


class PromoState(StatesGroup):
    start = State()
    invalid = State()
    adding_name = State()
    adding_file = State()
    save_file = State()
    question = State()
    delete_file = State()
    update_file = State()

