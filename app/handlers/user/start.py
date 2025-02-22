from aiogram import types
from aiogram.filters import CommandStart
from aiogram.filters.state import StateFilter

from app.handlers.bot_utils import menu
from app.handlers.msg_text import msg_text
from app.keyboards.default.create_profile import start_kb
from app.routers import start_router
from data.config import IMAGES_DIR
from database.models import UserModel


@start_router.message(CommandStart(), StateFilter(None))
async def _start_command(message: types.Message, user: UserModel) -> None:
    """Стратовая команда"""
    if user.profile:
        await menu(user.id)
    else:
        photo = types.FSInputFile(f"{IMAGES_DIR}/new_logo.webp")
        await message.answer_photo(
            photo=photo,
            caption=msg_text.WELCOME,
            reply_markup=start_kb(),
        )
