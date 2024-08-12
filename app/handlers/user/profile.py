from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import dp, bot
from app.keyboards.default import profile_kb
from database.service.profile import get_profile

menu_text = """
🔄 Заполнить анкету заново
🖼 Изменить фотографию
✍️ Изменить описание
❌ Удалить анкету
🔍 Смотреть анкеты
"""

@dp.message_handler(Text("👤"))
async def _profile_command(message: types.Message):
    user = await get_profile(message.from_user.id)
    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=user.photo,
        caption=f"{user.name}, {user.age}, {user.city}\n{user.description}",
    )
    await message.answer(
        menu_text,
        reply_markup=profile_kb(),
    )



