from aiogram.fsm.state import State, StatesGroup


class QuestionState(StatesGroup):
    start = State()
    question = State()
    ask_question_director = State()
    getting_question = State()
    question_list = State()
