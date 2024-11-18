from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

gender_map = {
    "Я парень": 'male',
    "I'm a boy": 'male',
    "Я хлопець": 'male',
    "Я девушка": 'female',
    "I'm a girl": 'female',
    "Я дівчина": 'female',
}

find_gender_map = {
    "Парни": 'male',
    "Boys": 'male',
    "Хлопці": 'male',
    "Девушки": 'female',
    "Girls": 'female',
    "Дівчата": 'female',
    "Все": 'all',
    "All": 'all',
    "Всі": 'all',
}
class Create(BoundFilter):
    async def check(self, message: Message):
        return bool(message.text in ["/create", "Создать анкету", "Create a profile", "Створити анкету"])


class Gender(BoundFilter):
    async def check(self, message: Message):
        if message.text in gender_map:
            message.conf['gender'] = gender_map[message.text]
            return True
        else:
            # await message.answer(msg_text.INVALID_RESPONSE)
            # есть возможнть таким образом реализовать ошибки, но проблема с языками
            return False
        
class FindGender(BoundFilter):
    async def check(self, message: Message):
        if message.text in find_gender_map:
            message.conf['find_gender'] = find_gender_map[message.text]
            return True
        else:
            return False
        
class Photo(BoundFilter):
    async def check(self, message: Message):
        return bool(message.photo)
            
class Name(BoundFilter):
    async def check(self, message: Message):
        return bool(len(message.text) < 70)

        
class Age(BoundFilter):
    async def check(self, message: Message):
        return bool(message.text.isdigit() and int(message.text) < 100 and int(message.text) > 6)

from utils.cordinate import get_coordinates
        
class City(BoundFilter):
    async def check(self, message: Message):
        coordinates = get_coordinates(message.text)
        if coordinates:
            message.conf['coordinates'] = coordinates
            return True      
        else:
            return False
        
class Description(BoundFilter):
    async def check(self, message: Message):
        return bool(len(message.text) < 300)
