from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message
from data.config import admins


class IsAdmin(BoundFilter):
    async def check(self, message: Message):
        if str(message.from_user.id) in admins:
            return True
        else:
            return False
        
