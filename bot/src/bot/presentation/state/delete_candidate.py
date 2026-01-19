from aiogram.fsm.state import State, StatesGroup


class DeleteCandidateState(StatesGroup):
    confirm = State()

