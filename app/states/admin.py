from aiogram.fsm.state import State, StatesGroup


class Mailing(StatesGroup):
    message = State()
