from aiogram.fsm.state import StatesGroup, State


class FaqState(StatesGroup):
    faq = State()
    answer = State()
    adding_question = State()
    adding_answer = State()
    adding_faq = State()
    deleted_faq = State()
