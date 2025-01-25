from aiogram import F, types

from app.routers import admin_router as router

from app.handlers.msg_text import msg_text
from app.filters.admin import IsAdmin


@router.message(IsAdmin(), F.text.in_(["📩 Рассылка", "📩 Mailing list", "📩 Розсилка"]))
async def _users_mailing_panel(message: types.Message) -> None:
    """Админ панель для рассылки пользователям"""
    await message.answer(msg_text.MAILING_PANEL)


"""unfinished"""
