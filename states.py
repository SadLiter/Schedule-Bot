from aiogram.fsm.state import State, StatesGroup

class Register(StatesGroup):
    group_number = State()
    today_day = State()