from aiogram.dispatcher.filters.state import StatesGroup, State


class ProfileStatesGroup(StatesGroup):
    gender = State()
    find_gender = State()
    photo = State()
    name = State()
    age = State()
    city = State()
    desc = State()