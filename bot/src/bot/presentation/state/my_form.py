from aiogram.fsm.state import StatesGroup, State


class MyDocumentState(StatesGroup):
    document = State()
    form = State()
    document_form = State()
    approval = State()
    document_approval = State()
    statement = State()
    document_statement = State()
