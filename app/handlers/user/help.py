from aiogram import types
from aiogram.filters import Command

from app.routers import user_router as router

from data.config import IMAGES_DIR

from app.handlers.msg_text import msg_text


@router.message(Command('help'))
async def _help_command(message: types.Message) -> None:
    """Команда дающее небольшое описание бота"""
    with open(f'{IMAGES_DIR}/logo.jpg', "rb") as photo:
        await message.answer_photo(photo=photo, caption=msg_text.INFO.format())
