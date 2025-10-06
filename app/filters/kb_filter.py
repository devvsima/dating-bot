from aiogram.filters.callback_data import CallbackData


class LangCallback(CallbackData, prefix="lang"):
    lang: str


class BlockUserCallback(CallbackData, prefix="ban"):
    complaint_id: int
    receiver_id: int
    receiver_username: str | None
    ban: bool


class StatsCallback(CallbackData, prefix="stats"):
    type: str
