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
    "Biarkan yang sebelumnya",  # Индонезийский (исправлено с "Biarkan sebelumnya")
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
    "Selesai, simpan foto",  # Индонезийский (исправлено с "Sudah, simpan foto")
)


class IsCreate(Filter):
    async def __call__(self, message: Message) -> bool:
        return bool(message.text in START_COMMAND_OPTIONS)


class IsGender(Filter):
    async def __call__(self, message: Message) -> dict | bool:
        if message.text in GENDER_MAP:
            return {"gender": GENDER_MAP[message.text]}
        return


class IsFindGender(Filter):
    async def __call__(self, message: Message) -> dict | bool:
        if message.text in FIND_GENDER_MAP:
            return {"find_gender": FIND_GENDER_MAP[message.text]}
        return False


class IsPhoto(Filter):
    async def __call__(self, message: Message) -> bool:
        return bool(
            message.photo
            or message.text in LEAVE_PREVIOUS_OPTIONS
            or message.text in SAVE_PHOTO_OPTIONS
        )


class IsName(Filter):
    async def __call__(self, message: Message) -> bool:
        return bool(len(message.text) < 70)


class IsAge(Filter):
    async def __call__(self, message: Message) -> bool:
        return bool(message.text.isdigit() and int(message.text) < 100 and int(message.text) > 6)


class IsCity(Filter):
    async def __call__(self, message: Message) -> bool:
        latitude: float = None
        longitude: float = None
        city: str = None
        is_shared_location: bool = None

        if message.location:
            latitude = message.location.latitude
            longitude = message.location.longitude
            city = get_city_name(latitude=latitude, longitude=longitude)
            is_shared_location = True
        if message.text:
            if message.text.isdigit() and len(message.text) <= 1:
                return False
            if message.text in LEAVE_PREVIOUS_OPTIONS:
                pass
            elif coordinates := get_coordinates(message.text):
                latitude = coordinates[0]
                longitude = coordinates[1]
                city = message.text
                is_shared_location = False
            else:
                return False

        return {
            "latitude": latitude,
            "longitude": longitude,
            "city": city,
            "is_shared_location": is_shared_location,
        }


class IsDescription(Filter):
    async def __call__(self, message: Message) -> bool:
        return bool(
            len(message.text) < 900 or message.text in SKIP_OPTIONS,
        )


class IsMessageToUser(Filter):
    async def __call__(self, message: Message) -> bool:
        return bool(len(message.text) < 250)
