from aiogram import F, types
from aiogram.filters.state import StateFilter

from app.handlers.message_text import user_message_text as umt
from app.routers import voide_router


@voide_router.message(F.text, StateFilter(None))
async def profile_command(message: types.Message) -> None:
    """Отвечает пользователю если никакие фильтры не сработали,
    тобиж на не известные команды"""
    await message.answer(umt.UNKNOWN_COMMAND)
