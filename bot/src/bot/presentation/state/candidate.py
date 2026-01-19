from aiogram.fsm.state import State, StatesGroup


class CandidateState(StatesGroup):
    type_recruitment = State()
    nationality = State()
    university = State()
    birthdate = State()
    surname = State()
    name = State()
    patronymic = State()
    military_station = State()
    field_study = State()
    average_score = State()
    find_out = State()
    phone_number = State()
    document = State()
