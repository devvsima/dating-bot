from aiogram import F, types
from aiogram.filters.state import StateFilter

from app.routers import voide_router
from app.text import message_text as mt


@voide_router.message(F.text, StateFilter(None))
async def profile_command(message: types.Message) -> None:
    """Отвечает пользователю если никакие фильтры не сработали,
    тобиж на не известные команды"""
    await message.answer(mt.UNKNOWN_COMMAND)
