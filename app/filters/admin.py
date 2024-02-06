from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message
from database.service.admin import get_admins


class IsAdmin(BoundFilter):
    async def check(self, message: Message):
        if str(message.from_user.id) in get_admins():
            return True
        else:
            return False
        
