from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from app.keyboards import yes_or_not
from database.service.users import elastic_search_user_ids, get_profile
from app.states.search_state import Search


@dp.message_handler(Text("🔍"))
async def search_command(message: types.Message):
    await message.answer("Идет поиск...",reply_markup= yes_or_not())
    await Search.search.set()
    # await search_profile("👎")
    

@dp.message_handler(Text(["👎"]), state=Search.search)
async def search_profile(message: types.Message, state=FSMContext):
    id_list = await elastic_search_user_ids(message.from_user.id)
    
    i = await get_profile(id_list[0])

    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=i.photo,
        caption=f"{i.name}, {i.age}, {i.city}\n{i.description}",
    )


@dp.message_handler(Text("💤"))
async def search_profile(message: types.Message):
    await Search.finish()