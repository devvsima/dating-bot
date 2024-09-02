from aiogram.dispatcher.filters.state import StatesGroup, State


class ProfileCreate(StatesGroup):
    gender = State()
    find_gender = State()
    photo = State()
    name = State()
    age = State()
    city = State()
    desc = State()
    
class ProfileEdit(StatesGroup):
    photo = State()
    desc = State()