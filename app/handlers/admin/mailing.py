from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import dp

from app.handlers.msg_text import msg_text
from app.filters.admin import IsAdmin

@dp.message_handler(IsAdmin(), Text(["📩 Рассылка", "📩 Mailing list", "📩 Розсилка"]))
async def _users_mailing_panel(message: types.Message) -> None:
    """Админ панель для рассылки пользователям"""
    await message.answer(msg_text.MAILING_PANEL)
    
"""unfinished"""