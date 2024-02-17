from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import dp, bot
from app.keyboards import yes_or_not
from database.service.users import elastic_search_city


@dp.message_handler(Text("🔍"))
async def search_comm(message: types.Message):
    
    profile = await elastic_search_city(message.from_user.id)
    # print(profile)
    for i in profile:
        print(i)

        await bot.send_photo(
            chat_id=message.from_user.id,
            photo=i.photo,
            caption=f"{i.name}, {i.age}, {i.city}\n{i.description}",
            reply_markup=yes_or_not(),
        )

