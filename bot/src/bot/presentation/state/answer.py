from aiogram.fsm.state import State, StatesGroup


class AnswerState(StatesGroup):
    start = State()
    invalid = State()
    save_answer = State()
