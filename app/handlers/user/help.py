from aiogram import types
from aiogram.filters import Command
from aiogram.filters.state import StateFilter

from app.routers import user_router as router

from data.config import IMAGES_DIR

from app.handlers.msg_text import msg_text


@router.message(Command("help"), StateFilter(None))
async def _help_command(message: types.Message) -> None:
    """Команда дающее небольшое описание бота"""
    photo = types.FSInputFile(f"{IMAGES_DIR}/new_logo.webp")
    await message.answer_photo(photo=photo, caption=msg_text.INFO)
