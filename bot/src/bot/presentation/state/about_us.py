from aiogram.fsm.state import StatesGroup, State


class AboutUsState(StatesGroup):
    about_us_url = State()
