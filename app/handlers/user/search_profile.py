from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from app.keyboards import yes_or_not
from database.service.users import elastic_search_user_ids, get_profile
from app.states.search_state import Search


@dp.message_handler(Text("🔍"))
async def search_command(message: types.Message, state: FSMContext):
    await message.answer("Идет поиск...",reply_markup= yes_or_not())
    async with state.proxy() as data:
        data["ids"] = await elastic_search_user_ids(message.from_user.id)
        data["index"] = 0

    await Search.search.set()
    await search_profile()
    

@dp.message_handler(Text(["❤️","👎"]), state=Search.search)
async def search_profile(message: types.Message, state=FSMContext):


    async with state.proxy() as data:
        ids = data['ids']

        if data['index'] >= len(ids):
            data['index'] = 0
        profile = await get_profile(ids[data['index']])
        if message.text == "❤️":
            index = data['index'] -1
            
            await bot.send_message(chat_id=ids[index], text="Кому-то понравилась ваша анкета")
        await bot.send_photo(
            chat_id=message.from_user.id,
            photo=profile.photo,
            caption=f"{profile.name}, {profile.age}, {profile.city}\n{profile.description}",
        )
        data['index'] += 1


@dp.message_handler(Text("💤"), state=Search.search)
async def search_profile(message: types.Message, state: FSMContext):
    await message.answer("вы вышли")
    await state.finish()