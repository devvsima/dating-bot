from aiogram import types, Dispatcher
from loader import dp, bot
from app.keyboards import yes_or_not
from database.users import find


@dp.message_handler(text="🔍")
async def profile_comm(message: types.Message):

    profile = await find(message.from_user.id)

    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=profile[0][3],
        caption=f"{profile[0][4]}, {profile[0][5]}, {profile[0][6]}\n{profile[0][7]}",
        reply_markup=yes_or_not(),
    )
    print(profile)
