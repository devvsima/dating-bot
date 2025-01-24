from aiogram.filters import Filter
from aiogram.types import Message
from data.config import ADMINS

class IsAdmin(Filter):
    async def __call__(self, message: Message):
        """Проверят пользователя на администраторские права"""
        return bool(int(message.from_user.id) in ADMINS)

        