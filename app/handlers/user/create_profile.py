from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp, bot

from database.service.profile import create_profile

from utils.cordinate import get_coordinates

from app.keyboards.default import cancel_kb, gender_kb, find_gender_kb
from app.states import ProfileStatesGroup
from .start import _start_command


@dp.message_handler(text="🔄")
async def _retry_create_profile_command(message: types.Message):
    await _create_profile_command(message)


# create profile
@dp.message_handler(Command("create"))
async def _create_profile_command(message: types.Message):
    await message.answer("Укажи свой пол:", reply_markup=gender_kb())
    await ProfileStatesGroup.gender.set()


# gender
@dp.message_handler(lambda message: message.text != "Я парень" and message.text != "Я девушка",
    state=ProfileStatesGroup.gender)
async def _gender_filter(message: types.Message):
    await message.answer("Некорректный ответ. Пожалуйста, выбери на клавиатуре или напиши правильно. 📝")


@dp.message_handler(state=ProfileStatesGroup.gender)
async def _gender(message: types.Message, state: FSMContext):
    if message.text == 'Я парень':
        gender = 'male'
    elif message.text == 'Я девушка':
        gender = 'female'

    async with state.proxy() as data:
        data["gender"] = gender
        await message.reply("Кто тебе больше интересен? Выбери пол человека: 👤", reply_markup=find_gender_kb())

    await ProfileStatesGroup.find_gender.set()


# gender of interest
@dp.message_handler(lambda message: message.text != "Парни" and message.text != "Девушки" and message.text != "Все",
    state=ProfileStatesGroup.find_gender)
async def _find_gender_filter(message: types.Message):
    await message.answer(text=("Некорректный ответ. Пожалуйста, выбери на клавиатуре или напиши правильно. 📝"))


@dp.message_handler(state=ProfileStatesGroup.find_gender)
async def _find_gender(message: types.Message, state: FSMContext):
    del_markup = types.ReplyKeyboardRemove()
    if message.text == 'Парни':
        gender = 'male'
    elif message.text == 'Девушки':
        gender = 'female'
    elif message.text == 'Все':
        gender = 'all'

    async with state.proxy() as data:
        data["find_gender"] = gender

    await message.reply(text=("Пришли свое фото!"), reply_markup=del_markup)
    await ProfileStatesGroup.next()


# photo
@dp.message_handler(lambda message: not message.photo,
    state=ProfileStatesGroup.photo)
async def _photo_filter(message: types.Message):
    await message.answer("Неверный формат фотографии! Пожалуйста, загрузите изображение в правильном формате. 🖼️")


@dp.message_handler(content_types=["photo"], state=ProfileStatesGroup.photo)
async def _photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["photo"] = message.photo[0].file_id
    await message.reply("Как тебя зовут? Напиши своё имя, чтобы мы могли продолжить! ✍️")
    await ProfileStatesGroup.next()


# name
@dp.message_handler(lambda message: len(message.text) > 70,
    state=ProfileStatesGroup.name)
async def _name_filter(message: types.Message):
    await message.answer("Превышен лимит символов. Пожалуйста, сократи сообщение. ✂️")


@dp.message_handler(state=ProfileStatesGroup.name)
async def _name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = message.text


    await message.reply("Сколько тебе лет? Укажи свой возраст, пожалуйста! 🎂")
    await ProfileStatesGroup.next()


# age
@dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 100,
    state=ProfileStatesGroup.age)
async def _age_filter(message: types.Message):
    await message.answer("Неверный формат, возраст нужно указывать цифрами. 🔢")
    


@dp.message_handler(state=ProfileStatesGroup.age)
async def _age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["age"] = message.text

        await message.reply("Теперь введи свой город. 🏙️")
        await ProfileStatesGroup.next()


# city
@dp.message_handler(lambda message: len(message.text) > 70, 
    state=ProfileStatesGroup.city,)
async def _city_filter(message: types.Message):
    await message.answer("Превышен лимит символов. Пожалуйста, сократи сообщение. ✂️")


@dp.message_handler(state=ProfileStatesGroup.city)
async def _city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["city"] = message.text
        data['latitude'], data['longitude'] = get_coordinates(message.text)
    
    await message.reply("Расскажи немного о себе! Это поможет другим лучше тебя узнать. 📝")
    await ProfileStatesGroup.next()
    


# description
@dp.message_handler(lambda message: len(message.text) > 250, 
    state=ProfileStatesGroup.desc)
async def _decription_filter(message: types.Message):
    await message.answer("Превышен лимит символов. Пожалуйста, сократи сообщение. ✂️")


@dp.message_handler(state=ProfileStatesGroup.desc)
async def _decription(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data["desc"] = message.text
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=data["photo"],
            caption=f'{data["name"]}, {data["age"]} | Город: {data["city"]}\n{data["desc"]}',
        )
    await ProfileStatesGroup.next()
    await create_profile(state, user_id=message.from_user.id)
    await _start_command(message)
