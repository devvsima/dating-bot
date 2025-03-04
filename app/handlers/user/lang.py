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
    """Отображает список доступных языков и позволяет выбрать предпочтительный"""
    await message.answer(msg_text.CHANGE_LANG, reply_markup=lang_ikb())


@router.callback_query(LangCallback.filter(), StateFilter(None))
async def _change_lang(
    callback: types.CallbackQuery, callback_data: LangCallback, user: UserModel, session
) -> None:
    """Обрабатывает выбранный пользователем язык, и устанавливает его"""
    await User.update_language(session, user, callback_data.lang)
    await callback.message.edit_text(msg_text.DONE_CHANGE_LANG)
