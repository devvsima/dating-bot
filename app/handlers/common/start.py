from aiogram import types
from aiogram.filters import CommandStart
from aiogram.filters.state import StateFilter

from app.handlers.bot_utils import menu
from app.handlers.message_text import user_message_text as umt
from app.keyboards.default.create_profile import start_kb
from app.routers import common_router
from data.config import IMAGES_DIR
from database.models import UserModel


@common_router.message(StateFilter(None), CommandStart())
async def _start_command(message: types.Message, user: UserModel) -> None:
    """Стандартная команда /start для запуска бота и начала взаимодействия с ним"""
    if user.profile:
        await menu(user.id)
    else:
        photo = types.FSInputFile(f"{IMAGES_DIR}/new_logo.webp")
        await message.answer_photo(
            photo=photo,
            caption=umt.WELCOME,
            reply_markup=start_kb(),
        )
