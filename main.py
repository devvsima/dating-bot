from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.callback_data import CallbackData
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State


# импорт скриптов
from database import *
from app import *
from config import *
from utils import *

storage = MemoryStorage()
bot = Bot(token_api)
dp = Dispatcher(bot=bot, storage=storage)


async def start_up(_):
    await db_start()
    print(" [ Бот запущен ] ")


# список ипорт данных от пользователя
class ProfileStatesGroup(StatesGroup):
    gender = State()
    find_gender = State()
    photo = State()
    name = State()
    age = State()
    city = State()
    desc = State()


class Test(BaseMiddleware):
    async def on_pre_process_update(self, update: types.update, data: dict):
        print("Действие")


# старт
@dp.message_handler(commands="start")
async def start_command(message: types.Message):
    await message.answer(
        text="Выбери язык: ",
        reply_markup=start_kb(),
    )
    await message.delete()


@dp.message_handler(text=("🏳️Русский", "🇺🇦Українська", "🇬🇧English"))
async def start_command(message: types.Message):
    await message.answer(
        text="Привет, теперь давай создадим тебе профиль! Для создание нажми или напиши '/create'",
        reply_markup=base_kb(),
    )
    await message.delete()


# выключение машины состояний
@dp.message_handler(commands="cancel", state="*")
async def com_cancel(message: types.message, state: FSMContext):
    if state is None:
        return
    await state.finish()
    await message.answer("Вы вышли с создания анкеты.")


# создание профиля
@dp.message_handler(commands="create")
async def photo(message: types.message):
    await ProfileStatesGroup.gender.set()
    await create_profile(user_id=message.from_user.id)
    reply_markup = cancel_kb()
    await message.reply("Выберете свой пол:", reply_markup=gender_kb())


# пол
@dp.message_handler(
    lambda message: len(message.text) > 70,
    state=ProfileStatesGroup.gender,
)
async def gender(message: types.Message):
    await message.answer("Превышен лимит символов.")


@dp.message_handler(state=ProfileStatesGroup.gender)
async def load_gender(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data["gender"] = message.text
        await message.reply("Кто тебе интересен", reply_markup=find_gender_kb())

    await ProfileStatesGroup.find_gender.set()


# интересующий пол
@dp.message_handler(
    lambda message: len(message.text) > 70,
    lambda message: len(message.text) == "Парни" and "Девушки",
    state=ProfileStatesGroup.find_gender,
)
# @dp.message_handler(
#     lambda message: len(message.text) == "Парни" and "Девушки",
#     state=ProfileStatesGroup.find_gender,
# )


async def find_gender(message: types.Message):
    await message.answer("Превышен лимит символов.")


@dp.message_handler(state=ProfileStatesGroup.find_gender)
async def load_find_gender(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data["find_gender"] = message.text
        await message.reply("Пришли свое фото!")

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
    await message.reply("Ну ты и урод сукааааа.")
    # await ProfileStatesGroup.next()


# старт скрипта
if __name__ == "__main__":
    dp.middleware.setup(Test())
    executor.start_polling(
        dp,
        on_startup=start_up,
        skip_updates=True,
    )
