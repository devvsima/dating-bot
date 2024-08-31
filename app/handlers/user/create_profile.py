from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp, bot

from database.service.profile import create_profile, edit_profile_photo, edit_profile_description

from utils.cordinate import get_coordinates

from app.keyboards.default import gender_kb, find_gender_kb, del_kb

from app.states.profile_create_state import ProfileStatesGroupRetry
from app.handlers.user.profile import _profile_command
from app.states import ProfileStatesGroup
from app.handlers import msg_text
from .cancel import _cancel_command



@dp.message_handler(text="🔄")
async def _retry_create_profile_command(message: types.Message):
    await _create_profile_command(message)


# create profile
@dp.message_handler(Command("create"))
async def _create_profile_command(message: types.Message):
    await message.answer(msg_text.GENDER, reply_markup=gender_kb())
    
    await ProfileStatesGroup.gender.set()


# gender
@dp.message_handler(lambda message: message.text != "Я парень" and message.text != "Я девушка", state=ProfileStatesGroup.gender)
async def _gender_filter(message: types.Message):
    await message.answer(msg_text.INVALID_RESPONSE)

@dp.message_handler(state=ProfileStatesGroup.gender)
async def _gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["gender"] = {'Я парень': 'male', 'Я девушка': 'female'}[message.text]
        
    await message.reply(msg_text.FIND_GENDER, reply_markup=find_gender_kb())
    await ProfileStatesGroup.find_gender.set()


# gender of interest
@dp.message_handler(lambda message: message.text != "Парни" and message.text != "Девушки" and message.text != "Все",
    state=ProfileStatesGroup.find_gender)
async def _find_gender_filter(message: types.Message):
    await message.answer(msg_text.INVALID_RESPONSE)

@dp.message_handler(state=ProfileStatesGroup.find_gender)
async def _find_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["find_gender"] = {'Парни': 'male', 'Девушки': 'female', 'Все': 'all'}[message.text]

    await message.reply(msg_text.PHOTO, reply_markup=del_kb)
    await ProfileStatesGroup.next()

# photo
@dp.message_handler(lambda message: not message.photo, state=[ProfileStatesGroupRetry.photo, ProfileStatesGroup.photo])
async def _photo_filter(message: types.Message):
    await message.answer(msg_text.INVALID_PHOTO)

@dp.message_handler(content_types=["photo"], state=[ProfileStatesGroupRetry.photo, ProfileStatesGroup.photo])
async def _photo(message: types.Message, state: FSMContext):
    photo = message.photo[0].file_id
    if await state.get_state() == ProfileStatesGroupRetry.photo.state:
        await edit_profile_photo(message.from_user.id, photo)
        await _profile_command(message)
        await state.finish()
    
    async with state.proxy() as data:
        data["photo"] = photo
        
    await message.reply(msg_text.NAME)
    await ProfileStatesGroup.next()


# name
@dp.message_handler(lambda message: len(message.text) > 70,
    state=ProfileStatesGroup.name)
async def _name_filter(message: types.Message):
    await message.answer(msg_text.INVALID_LONG_RESPONSE)


@dp.message_handler(state=ProfileStatesGroup.name)
async def _name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = message.text

    await message.reply(msg_text.AGE)
    await ProfileStatesGroup.next()


# age
@dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 100, state=ProfileStatesGroup.age)
async def _age_filter(message: types.Message):
    await message.answer(msg_text.INVALID_AGE)


@dp.message_handler(state=ProfileStatesGroup.age)
async def _age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["age"] = message.text

        await message.reply(msg_text.CITY)
        await ProfileStatesGroup.next()


# city
@dp.message_handler(lambda message: len(message.text) > 70, 
    state=ProfileStatesGroup.city,)
async def _city_filter(message: types.Message):
    await message.answer(msg_text.INVALID_LONG_RESPONSE)


@dp.message_handler(state=ProfileStatesGroup.city)
async def _city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["city"] = message.text
        data['latitude'], data['longitude'] = get_coordinates(message.text)
    
    await message.reply(msg_text.DESCRIPTION)
    await ProfileStatesGroup.next()
    


# description
@dp.message_handler(lambda message: len(message.text) > 250, state=[ProfileStatesGroup.desc, ProfileStatesGroupRetry.desc])
async def _decription_filter(message: types.Message):
    await message.answer(msg_text.INVALID_LONG_RESPONSE)

@dp.message_handler(state=[ProfileStatesGroup.desc, ProfileStatesGroupRetry.desc])
async def _decription(message: types.Message, state=FSMContext):
    if await state.get_state() == ProfileStatesGroupRetry.desc.state:
        await edit_profile_description(message.from_user.id, message.text)
        await _profile_command(message)
        await state.finish()
        return
    
    async with state.proxy() as data:
        data["desc"] = message.text
        
    await create_profile(state, user_id=message.from_user.id)
    await ProfileStatesGroup.next()
    await _profile_command(message)
