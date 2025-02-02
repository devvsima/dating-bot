from aiogram.filters import Filter
from aiogram.types import Message

from utils.cordinate import get_coordinates

gender_map = {
    "Я парень": "male",
    "I'm male": "male",
    "Я хлопець": "male",
    "Я девушка": "female",
    "I'm female": "female",
    "Я дівчина": "female",
}

find_gender_map = {
    "Парни": "male",
    "Male": "male",
    "Men": "male",
    "Девушки": "female",
    "Women": "female",
    "Дівчата": "female",
    "Все": "all",
    "All": "all",
    "Всі": "all",
}


class IsCreate(Filter):
    async def __call__(self, message: Message) -> bool:
        return bool(
            message.text in ["/create", "Создать анкету", "Create a profile", "Створити анкету"]
        )


class IsGender(Filter):
    async def __call__(self, message: Message) -> dict | bool:
        if message.text in gender_map:
            return {"gender": gender_map[message.text]}
        return


class IsFindGender(Filter):
    async def __call__(self, message: Message) -> dict | bool:
        if message.text in find_gender_map:
            return {"find_gender": find_gender_map[message.text]}
        return False


class IsPhoto(Filter):
    async def __call__(self, message: Message) -> bool:
        return bool(message.photo)


class IsName(Filter):
    async def __call__(self, message: Message) -> bool:
        return bool(len(message.text) < 70)


class IsAge(Filter):
    async def __call__(self, message: Message) -> bool:
        return bool(message.text.isdigit() and int(message.text) < 100 and int(message.text) > 6)


class IsCity(Filter):
    async def __call__(self, message: Message) -> bool:
        if message.text.isdigit():
            return False
        elif coordinates := get_coordinates(message.text):
            return {"coordinates": coordinates}
        return False


class IsDescription(Filter):
    async def __call__(self, message: Message) -> bool:
        return bool(len(message.text) < 1000)
