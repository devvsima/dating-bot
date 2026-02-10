from aiogram import F, types
from aiogram.filters.state import StateFilter

from app.routers import voide_router
from app.text import message_text as mt
from database.models.user import User


@voide_router.message(StateFilter("*"), F.text)
async def profile_command(message: types.Message, user: User) -> None:
    """Отвечает пользователю если никакие фильтры не сработали,
    тобиж на не известные команды"""
    await message.answer(mt.UNKNOWN_COMMAND(language=user.language))
