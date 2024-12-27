from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

from utils.cordinate import get_coordinates

gender_map = {
    "Я парень": 'male',
    "I'm male": 'male',
    "Я хлопець": 'male',
    "Я девушка": 'female',
    "I'm female": 'female',
    "Я дівчина": 'female',
}

find_gender_map = {
    "Парни": 'male',
    "Male": 'male',
    "Men": 'male',
    "Девушки": 'female',
    "Women": 'female',
    "Дівчата": 'female',
    "Все": 'all',
    "All": 'all',
    "Всі": 'all',
}
class IsCreate(BoundFilter):
    async def check(self, message: Message) -> bool:
        return bool(message.text in ["/create", "Создать анкету", "Create a profile", "Створити анкету"])


class IsGender(BoundFilter):
    async def check(self, message: Message) -> bool:
        if message.text in gender_map:
            message.conf['gender'] = gender_map[message.text]
            return True
        return False
        
class IsFindGender(BoundFilter):
    async def check(self, message: Message) -> bool:
        if message.text in find_gender_map:
            message.conf['find_gender'] = find_gender_map[message.text]
            return True
        return False
        
class IsPhoto(BoundFilter):
    async def check(self, message: Message) -> bool:
        return bool(message.photo)
            
class IsName(BoundFilter):
    async def check(self, message: Message) -> bool:
        return bool(len(message.text) < 70)

        
class IsAge(BoundFilter):
    async def check(self, message: Message) -> bool:
        return bool(message.text.isdigit() and int(message.text) < 100 and int(message.text) > 6)

class IsCity(BoundFilter):
    async def check(self, message: Message) -> bool:
        coordinates = get_coordinates(message.text)
        if coordinates:
            message.conf['coordinates'] = coordinates
            return True
        return False
        
class IsDescription(BoundFilter):
    async def check(self, message: Message) -> bool:
        return bool(len(message.text) < 300)
