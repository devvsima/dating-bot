from aiogram import types
from aiogram.filters import Command
from aiogram.filters.state import StateFilter

from app.handlers.message_text import user_message_text as umt
from app.routers import user_router as router
from data.config import IMAGES_DIR


@router.message(Command("info"), StateFilter(None))
@router.message(Command("help"), StateFilter(None))
async def _help_command(message: types.Message) -> None:
    """Отправляет пользователю небольшое описание бота"""
    photo = types.FSInputFile(f"{IMAGES_DIR}/new_logo.webp")
    await message.answer_photo(photo=photo, caption=umt.INFO)
