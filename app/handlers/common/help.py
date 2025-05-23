from aiogram import types
from aiogram.filters import Command
from aiogram.filters.state import StateFilter

from app.handlers.message_text import user_message_text as umt
from app.routers import common_router
from data.config import LOGO_DIR


@common_router.message(StateFilter(None), Command("info"))
@common_router.message(StateFilter(None), Command("help"))
async def _help_command(message: types.Message) -> None:
    """Отправляет пользователю небольшое описание бота"""
    photo = types.FSInputFile(LOGO_DIR)
    await message.answer_photo(photo=photo, caption=umt.INFO)
