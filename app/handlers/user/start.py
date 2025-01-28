from aiogram import types
from aiogram.filters import CommandStart
from aiogram.filters.state import StateFilter

from app.routers import start_router

from data.config import IMAGES_DIR

from database.service.profile import get_profile

from app.handlers.msg_text import msg_text
from app.keyboards.default import start_kb
from app.handlers.bot_utils import menu


photo = types.FSInputFile(f"{IMAGES_DIR}/new_logo.webp")


@start_router.message(CommandStart(), StateFilter(None))
async def _start_command(message: types.Message) -> None:
    """Стратовая команда"""
    if await get_profile(message.from_user.id):
        await menu(message.from_user.id)
    else:
        await message.answer_photo(
            photo=photo, caption=msg_text.WELCOME, reply_markup=start_kb()
        )
