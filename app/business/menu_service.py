from app.keyboards.default.base import menu_kb
from app.text import message_text as mt
from loader import bot


async def menu(chat_id: int) -> None:
    """Отправляет меню пользователю"""
    await bot.send_message(
        chat_id=chat_id,
        text=mt.MENU,
        reply_markup=menu_kb,
    )
