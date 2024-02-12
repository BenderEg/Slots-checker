from aiogram.filters.state import State, StatesGroup


class FSMmodel(StatesGroup):
    captcha = State()
