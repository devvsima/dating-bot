from aiogram import types, Dispatcher
from loader import dp, bot
from aiogram.dispatcher import FSMContext
from app.keyboards import cancel_kb, gender_kb, find_gender_kb
from database.bd import create_profile, edit_profile
from .start import lang_command
from app.states import ProfileStatesGroup


# создание профиля
@dp.message_handler(commands="create")
async def gender(message: types.message):
    await ProfileStatesGroup.gender.set()
    await create_profile(user_id=message.from_user.id)
    reply_markup = cancel_kb()
    await message.reply("Выберете свой пол:", reply_markup=gender_kb())


# пол
@dp.message_handler(
    lambda message: message.text != "Я парень" and message.text != "Я девушка",
    state=ProfileStatesGroup.gender,
)
async def find_gender(message: types.Message):
    await message.answer(
        "Не коректный ответ. Выберете на клавиатуре, или напичатайте парвильно."
    )


@dp.message_handler(state=ProfileStatesGroup.gender)
async def load_gender(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data["gender"] = message.text
        await message.reply("Кто тебе интересен", reply_markup=find_gender_kb())

    await ProfileStatesGroup.find_gender.set()


# интересующий пол
@dp.message_handler(
    lambda message: message.text != "Парни"
    and message.text != "Девушки"
    and message.text != "Все",
    state=ProfileStatesGroup.find_gender,
)
async def find_gender(message: types.Message):
    await message.answer(
        "Не коректный ответ. Выберете на клавиатуре, или напичатайте парвильно."
    )


@dp.message_handler(state=ProfileStatesGroup.find_gender)
async def load_find_gender(message: types.Message, state=FSMContext):
    del_markup = types.ReplyKeyboardRemove()
    async with state.proxy() as data:
        data["find_gender"] = message.text

        await message.reply("Пришли свое фото!", reply_markup=del_markup)
    await ProfileStatesGroup.next()


# фото
@dp.message_handler(lambda message: not message.photo, state=ProfileStatesGroup.photo)
async def check_photo(message: types.Message):
    await message.answer("Неверный формат фотографии!")


@dp.message_handler(content_types=["photo"], state=ProfileStatesGroup.photo)
async def load_photo(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data["photo"] = message.photo[0].file_id

    await message.reply("Как тебя зовут?")
    await ProfileStatesGroup.next()


# имя
@dp.message_handler(
    lambda message: len(message.text) > 70,
    state=ProfileStatesGroup.name,
)
async def check_age(message: types.Message):
    await message.answer("Превышен лимит символов.")


@dp.message_handler(state=ProfileStatesGroup.name)
async def load_name(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data["name"] = message.text

    await message.reply("Сколько тебе лет?")
    await ProfileStatesGroup.next()


# возраст
@dp.message_handler(
    lambda message: not message.text.isdigit() or float(message.text) > 100,
    state=ProfileStatesGroup.age,
)
async def check_age(message: types.Message):
    if message.text != 100:
        await message.answer("Неверный формат, возраст нужно писать цифрами.")
    elif float(message.text) > 100:
        await message.answer("К сожалению вы мертвы, введите реальный отзыв.")


@dp.message_handler(state=ProfileStatesGroup.age)
async def load_age(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data["age"] = message.text

        await message.reply("Теперь введи свой город.")
        await ProfileStatesGroup.next()


# город
@dp.message_handler(
    lambda message: len(message.text) > 70,
    state=ProfileStatesGroup.city,
)
async def check_age(message: types.Message):
    await message.answer("Превышен лимит символов.")


@dp.message_handler(state=ProfileStatesGroup.city)
async def load_city(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data["city"] = message.text

    await message.reply("Раскжи о себе.")
    await ProfileStatesGroup.next()


# описанние
@dp.message_handler(
    lambda message: len(message.text) > 250,
    state=ProfileStatesGroup.desc,
)
async def check_desc(message: types.Message):
    await message.answer("Превышен лимит символов.")


@dp.message_handler(state=ProfileStatesGroup.desc)
async def load_desc(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data["desc"] = message.text
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=data["photo"],
            caption=f'{data["name"]}, {data["age"]} | Город: {data["city"]}\n{data["desc"]}',
        )
    await edit_profile(state, user_id=message.from_user.id)

    await lang_command(message)
    await ProfileStatesGroup.next()
