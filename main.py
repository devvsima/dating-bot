from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.callback_data import CallbackData
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State


from bd import db_start, create_profile, edit_profile

# импорт скриптов
from config import token_api
from keyboard import base_kb, cancel_kb


storage = MemoryStorage()
bot = Bot(token_api)
dp = Dispatcher(bot=bot, storage=storage)


async def start_up(_):
    await db_start()
    print(" [ Бот запущен ] ")


# список ипорт данных от пользователя
class ProfileStatesGroup(StatesGroup):
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
        text="Здраствуйте, для того чтобы начать нужно написать команду '/create'.",
        reply_markup=base_kb,
    )
    await message.delete()
    await create_profile(user_id=message.from_user.id)


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
    await message.reply(
        "Давай создадим тебе профиль! Пришли свое фото.", reply_markup=cancel_kb
    )
    await ProfileStatesGroup.photo.set()


# фото
@dp.message_handler(lambda message: not message.photo, state=ProfileStatesGroup.photo)
async def check_photo(message: types.Message):
    await message.answer("Неверный формат фотографии!")


@dp.message_handler(content_types=["photo"], state=ProfileStatesGroup.photo)
async def load_photo(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data["photo"] = message.photo[0].file_id

    await message.reply("Теперь введи свое имя.\n(до 70 символов)")
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

    await message.reply("Теперь введи свой возраст.")
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

        await message.reply("Теперь введи свой город.\n(до 70 символов)")
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

    await message.reply("Теперь напиши о себе.")
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
    await ProfileStatesGroup.next()


# старт скрипта
if __name__ == "__main__":
    dp.middleware.setup(Test())
    executor.start_polling(
        dp,
        on_startup=start_up,
        skip_updates=True,
    )
