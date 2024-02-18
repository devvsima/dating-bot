from aiogram.dispatcher.filters.state import StatesGroup, State


class Search(StatesGroup):
    search = State()
