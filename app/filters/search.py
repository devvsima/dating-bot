from aiogram.filters import Filter
from aiogram.types import Message


class SearchFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        return bool(message.text in ("❤️", "👎", "💢", "🔞", "💰", "🔫", "↩️"))
