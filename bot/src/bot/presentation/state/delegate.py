from aiogram.fsm.state import State, StatesGroup


class RegistrationDelegateState(StatesGroup):
    start = State()
    last_name = State()
    first_name = State()
    patronymic = State()
    post = State()
    subject = State()
    start_date = State()
    invalid_start_date = State()
    end_date = State()
    invalid_end_date = State()
    finish = State()
