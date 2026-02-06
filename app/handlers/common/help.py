from aiogram import types
from aiogram.filters import Command
from aiogram.filters.state import StateFilter

from app.routers import common_router
from app.text import message_text as mt
from data.config import LOGO


@common_router.message(StateFilter(None), Command("info"))
@common_router.message(StateFilter(None), Command("help"))
async def _help_command(message: types.Message) -> None:
    """Отправляет пользователю небольшое описание бота"""
    await message.answer_photo(photo=LOGO, caption=mt.INFO)
