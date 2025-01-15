from aiogram import types
from aiogram.dispatcher.filters import Command, Text

from loader import dp

from database.service.users import change_language

from app.handlers.msg_text import msg_text
from app.keyboards.inline.lang import lang_ikb


@dp.message_handler(Command('language'))
@dp.message_handler(Command('lang'))
async def _lang(message: types.Message) -> None:
    """Предлагает клавиатуру с доступными языками"""
    await message.answer(msg_text.CHANGE_LANG, reply_markup=lang_ikb())

@dp.callback_query_handler(Text(['ru', 'uk', 'en']))
async def _lang_change(callback: types.CallbackQuery) -> None:
    """Меняет язык пользователя на выбранный"""
    change_language(callback.from_user.id, callback.data)
    await callback.message.edit_text(msg_text.DONE_CHANGE_LANG)
