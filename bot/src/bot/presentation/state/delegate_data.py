from aiogram.fsm.state import StatesGroup, State


class DelegateDataState(StatesGroup):
    start = State()
    first_name = State()
    patronymic = State()
    last_name = State()
    post = State()
    subject = State()
    start_date = State()
    invalid_start_date = State()
    end_date = State()
    invalid_end_date = State()
    save = State()
