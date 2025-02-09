from aiogram import F, types
from aiogram.filters import Command
from aiogram.filters.state import StateFilter

from app.handlers.msg_text import msg_text
from app.keyboards.inline.lang import lang_ikb
from app.routers import user_router as router
from database.models import UserModel
from database.services import User


@router.message(Command("language"), StateFilter(None))
@router.message(Command("lang"), StateFilter(None))
async def _lang(message: types.Message) -> None:
    """Предлагает клавиатуру с доступными языками"""
    await message.answer(msg_text.CHANGE_LANG, reply_markup=lang_ikb())


@router.callback_query(F.data.in_(["ru", "uk", "en"]))
async def _lang_change(callback: types.CallbackQuery, user: UserModel, session) -> None:
    """Меняет язык пользователя на выбранный"""
    await User.update_language(session, user=user, language=callback.data)
    await callback.message.edit_text(msg_text.DONE_CHANGE_LANG)
