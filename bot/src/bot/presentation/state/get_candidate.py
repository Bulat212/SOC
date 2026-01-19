from aiogram.fsm.state import StatesGroup, State


class GetCandidateState(StatesGroup):
    recruitment = State()
    candidate_list = State()

