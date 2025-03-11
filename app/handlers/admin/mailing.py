from aiogram import F, types
from aiogram.filters.state import StateFilter

from app.handlers.message_text import admin_message_text as amt
from app.routers import admin_router as router


@router.message(F.text == "📩 Mailing to users", StateFilter(None))
async def _users_mailing_panel(message: types.Message) -> None:
    """Админ панель для рассылки пользователям"""
    await message.answer(amt.MAILING_PANEL)


"""unfinished"""
