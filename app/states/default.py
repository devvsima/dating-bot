from aiogram.fsm.state import State, StatesGroup


class LikeResponse(StatesGroup):
    response = State()


class ProfileCreate(StatesGroup):
    name = State()
    gender = State()
    find_gender = State()
    age = State()
    city = State()
    photo = State()
    description = State()


class ProfileEdit(StatesGroup):
    photo = State()
    description = State()


class Search(StatesGroup):
    search = State()
    message = State()
