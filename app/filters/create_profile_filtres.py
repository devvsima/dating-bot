from aiogram.filters import Filter
from aiogram.types import Message

from utils.geopy import get_coordinates

gender_map = {
    "Парень": "male",  # Русский
    "Хлопець": "male",  # Украинский
    "Boy": "male",  # Английский
    "Garçon": "male",  # Французский
    "Chico": "male",  # Испанский
    "Chłopak": "male",  # Польский
    "Девушка": "female",  # Русский
    "Дівчина": "female",  # Украинский
    "Girl": "female",  # Английский
    "Fille": "female",  # Французский
    "Chica": "female",  # Испанский
    "Dziewczyna": "female",  # Польский
}

find_gender_map = {
    "Парней": "male",  # Русский
    "Хлопців": "male",  # Украинский
    "Boys": "male",  # Английский
    "Garçons": "male",  # Французский
    "Chicos": "male",  # Испанский
    "Chłopców": "male",  # Польский
    "Девушек": "female",  # Русский
    "Дівчат": "female",  # Украинский
    "Girls": "female",  # Английский
    "Filles": "female",  # Французский
    "Chicas": "female",  # Испанский
    "Dziewcząt": "female",  # Польский
    "Всех": "all",  # Русский
    "Усіх": "all",  # Украинский
    "Everyone": "all",  # Английский
    "Tous": "all",  # Французский
    "Todos": "all",  # Испанский
    "Wszyscy": "all",  # Польский
}


leave_previous_tuple = (
    "Оставить предыдущее",  # Русский
    "Leave previous",  # Английский
    "Залишити попереднє",  # Украинский
    "Laisser le précédent",  # Французский
    "Dejar el anterior",  # Испанский
    "Pozostaw poprzednie",  # Польский
)

start_command_tuple = (
    "/create",
    "Создать анкету",  # Русский
    "Create a profile",  # Английский
    "Створити анкету",  # Украинский
    "Créer un profil",  # Французский
    "Crear un perfil",  # Испанский
    "Utwórz profil",  # Польский
)


class IsCreate(Filter):
    async def __call__(self, message: Message) -> bool:
        return bool(message.text in start_command_tuple)


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
        return bool(message.photo or message.text in leave_previous_tuple)


class IsName(Filter):
    async def __call__(self, message: Message) -> bool:
        return bool(len(message.text) < 70)


class IsAge(Filter):
    async def __call__(self, message: Message) -> bool:
        return bool(message.text.isdigit() and int(message.text) < 100 and int(message.text) > 6)


class IsCity(Filter):
    async def __call__(self, message: Message) -> bool:
        if message.location:
            latitude = message.location.latitude
            longitude = message.location.longitude
        if message.text:
            if message.text.isdigit():
                return False
            if message.text in leave_previous_tuple:
                latitude = None
                longitude = None
            elif coordinates := get_coordinates(message.text):
                latitude = coordinates[0]
                longitude = coordinates[1]
            else:
                return False

        return {
            "latitude": latitude,
            "longitude": longitude,
        }


class IsDescription(Filter):
    async def __call__(self, message: Message) -> bool:
        return bool(len(message.text) < 900)
