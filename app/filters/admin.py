from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message
from data.config import ADMINS

class Admin(BoundFilter):
    async def check(self, message: Message):
        return bool(int(message.from_user.id) in ADMINS)

        