from aiogram import types
from aiogram.filters import Command
from aiogram.filters.state import StateFilter

from app.handlers.msg_text import msg_text
from app.keyboards.inline.lang import LangCallback, lang_ikb
from app.routers import user_router as router
from database.models import UserModel
from database.services import User


@router.message(Command("language"), StateFilter(None))
@router.message(Command("lang"), StateFilter(None))
async def _lang(message: types.Message) -> None:
    """Предлагает клавиатуру с доступными языками"""
    await message.answer(msg_text.CHANGE_LANG, reply_markup=lang_ikb())


@router.callback_query(LangCallback.filter())
async def _lang_change(
    callback: types.CallbackQuery, callback_data: LangCallback, user: UserModel, session
) -> None:
    """Меняет язык пользователя на выбранный"""
    await User.update_language(session, user, language=callback_data.lang)
    await callback.message.edit_text(msg_text.DONE_CHANGE_LANG)
