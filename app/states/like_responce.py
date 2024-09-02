from aiogram.dispatcher.filters.state import StatesGroup, State


class LikeResponse(StatesGroup):
    response = State()
