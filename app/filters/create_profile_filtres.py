from aiogram.filters import Filter
from aiogram.types import Message

from utils.geopy import get_city_name, get_coordinates

GENDER_MAP = {
    "Парень": "male",  # Русский
    "Хлопець": "male",  # Украинский
    "Boy": "male",  # Английский
    "Garçon": "male",  # Французский
    "Chico": "male",  # Испанский
    "Chłopak": "male",  # Польский
    "Laki-laki": "male",  # Индонезийский
    "Девушка": "female",  # Русский
    "Дівчина": "female",  # Украинский
    "Girl": "female",  # Английский
    "Fille": "female",  # Французский
    "Chica": "female",  # Испанский
    "Dziewczyna": "female",  # Польский
    "Perempuan": "female",  # Индонезийский
}

FIND_GENDER_MAP = {
    "Парней": "male",  # Русский
    "Хлопців": "male",  # Украинский
    "Boys": "male",  # Английский
    "Garçons": "male",  # Французский
    "Chicos": "male",  # Испанский
    "Chłopców": "male",  # Польский
    "Laki-laki": "male",  # Индонезийский (множественное число такое же)
    "Девушек": "female",  # Русский
    "Дівчат": "female",  # Украинский
    "Girls": "female",  # Английский
    "Filles": "female",  # Французский
    "Chicas": "female",  # Испанский
    "Dziewcząt": "female",  # Польский
    "Perempuan": "female",  # Индонезийский (множественное число такое же)
    "Всех": "all",  # Русский
    "Усіх": "all",  # Украинский
    "Everyone": "all",  # Английский
    "Tous": "all",  # Французский
    "Todos": "all",  # Испанский
    "Wszyscy": "all",  # Польский
    "Semua": "all",  # Индонезийский
}

LEAVE_PREVIOUS_OPTIONS = (
    "Оставить предыдущее",  # Русский
    "Leave previous",  # Английский
    "Залишити попереднє",  # Украинский
    "Laisser le précédent",  # Французский
    "Dejar el anterior",  # Испанский
    "Pozostaw poprzednie",  # Польский
    "Biarkan yang sebelumnya",  # Индонезийский
)

SKIP_OPTIONS = (
    "Пропустить",  # Русский
    "Skip",  # Английский
    "Пропустити",  # Украинский
    "Passer",  # Французский
    "Saltar",  # Испанский
    "Pomiń",  # Польский
    "Lewati",  # Индонезийский
)

START_COMMAND_OPTIONS = (
    "/create",
    "Создать анкету",  # Русский
    "Create a profile",  # Английский
    "Створити анкету",  # Украинский
    "Créer un profil",  # Французский
    "Crear un perfil",  # Испанский
    "Utwórz profil",  # Польский
    "Buat profil",  # Индонезийский
)

SAVE_PHOTO_OPTIONS = (
    "Это все, сохранить фото",  # Русский
    "That's it, keep the photo",  # Английский
    "Це все, зберегти фото",  # Украинский
    "C'est tout, gardez la photo",  # Французский
    "Eso es todo, guardar foto",  # Испанский
    "To wszystko, zachowaj zdjęcie",  # Польский
    "Selesai, simpan foto",  # Індонезійський
)


class IsCreate(Filter):
    async def __call__(self, message: Message) -> bool:
        return bool(message.text and message.text in START_COMMAND_OPTIONS)


class IsGender(Filter):
    async def __call__(self, message: Message) -> dict | bool:
        if not message.text:
            return False
        if message.text in GENDER_MAP:
            return {"gender": GENDER_MAP[message.text]}
        return False


class IsFindGender(Filter):
    async def __call__(self, message: Message) -> dict | bool:
        if not message.text:
            return False
        if message.text in FIND_GENDER_MAP:
            return {"find_gender": FIND_GENDER_MAP[message.text]}
        return False


class IsPhoto(Filter):
    async def __call__(self, message: Message) -> bool:
        return bool(
            message.photo
            or (message.text and message.text in LEAVE_PREVIOUS_OPTIONS)
            or (message.text and message.text in SAVE_PHOTO_OPTIONS)
        )


class IsName(Filter):
    async def __call__(self, message: Message) -> bool:
        if not message.text:
            return False
        return bool(len(message.text) < 70 and len(message.text) > 3)


class IsAge(Filter):
    async def __call__(self, message: Message) -> bool:
        if not message.text:
            return False
        return bool(message.text.isdigit() and int(message.text) < 100 and int(message.text) > 6)


class IsCity(Filter):
    async def __call__(self, message: Message) -> bool | dict:
        # Случай 1: Пользователь хочет оставить предыдущий город
        if message.text and message.text in LEAVE_PREVIOUS_OPTIONS:
            return {
                "use_previous": True,
                "latitude": None,
                "longitude": None,
                "city": None,
                "is_shared_location": None,
            }

        # Случай 2: Пользователь отправил геолокацию
        if message.location:
            latitude = message.location.latitude
            longitude = message.location.longitude
            city = get_city_name(latitude=latitude, longitude=longitude)
            return {
                "use_previous": False,
                "latitude": latitude,
                "longitude": longitude,
                "city": city,
                "is_shared_location": True,
            }

        # Случай 3: Пользователь ввел название города текстом
        if message.text:
            if message.text.isdigit() or len(message.text) <= 3:
                return False

            if coordinates := get_coordinates(message.text):
                return {
                    "use_previous": False,
                    "latitude": coordinates[0],
                    "longitude": coordinates[1],
                    "city": message.text,
                    "is_shared_location": False,
                }

            # Город не найден
            return False

        # Ничего не подошло
        return False


class IsDescription(Filter):
    async def __call__(self, message: Message) -> bool:
        if not message.text:
            return False
        return len(message.text) < 900 or message.text in SKIP_OPTIONS


class IsMessageToUser(Filter):
    async def __call__(self, message: Message) -> bool:
        return bool(len(message.text) < 250)
