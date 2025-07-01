from aiogram.fsm.state import State, StatesGroup


class LikeResponse(StatesGroup):
    response = State()


class ProfileCreate(StatesGroup):
    gender = State()
    find_gender = State()
    photo = State()
    name = State()
    age = State()
    city = State()
    description = State()


class ProfileEdit(StatesGroup):
    photo = State()
    description = State()


class Search(StatesGroup):
    search = State()
    message = State()
