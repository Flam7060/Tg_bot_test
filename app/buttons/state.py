from aiogram.fsm.state import State, StatesGroup

class ServicesState(StatesGroup):
    sevrice_id = State()
    name = State()
    phone = State()
    message = State()