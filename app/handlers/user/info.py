from aiogram import types
from aiogram.dispatcher.filters import Command, Text

from loader import dp, bot

from app.keyboards.default import  base_kb
from .menu import _menu

text = """
👋
Немного информации о боте:
Этот бот был создан по аналогии с популярным ботом для знакомств <a href='https://t.me/leomatchbot?start=i_VwRd0'>Дайвинчик</a>
Весь код бота открыт и доступен на <a href='https://github.com/devvsima/dating-bot'>GitHub</a>
Некотрую статистику можно глянуть по команде /stats

По вопросам и предложениям можно писать сюда: @devvsima.
"""

@dp.message_handler(Command('info'))
async def _start_command(message: types.Message):
    from data.config import DIR
    with open(f'{DIR}/photo/logo.jpg', "rb") as photo:
    
        await message.answer_photo(
            photo=photo,
            caption=(text),
        )
