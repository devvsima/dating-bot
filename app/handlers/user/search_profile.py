from aiogram import types, Dispatcher
from loader import dp, bot
from app.keyboards import yes_or_not
from database.bd import search_profile


@dp.message_handler(text="🔍")
async def profile_comm(message: types.Message):
    profile = search_profile(message.from_user.id)
    p = profile[0]

    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=profile[0][3],
        caption=f"{p[4]}, {p[5]}, {p[6]}\n{p[7]}",
        reply_markup=yes_or_not(),
    )
    print(profile)
