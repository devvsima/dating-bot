from aiogram import types, Dispatcher
from loader import dp, bot
from app.keyboards import yes_or_not
from database.service.users import find_user_id,find_user


@dp.message_handler(text="🔍")
async def search_comm(message: types.Message):

    user_ids = await find_user_id(message.from_user.id)
    profile = await find_user(user_ids[1])
    
    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=profile['photo'],
        caption=f"{profile['name']}, {profile['age']}, {profile['city']}\n{profile['description']}",
        reply_markup=yes_or_not(),
    )

