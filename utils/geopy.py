from geopy.geocoders import Nominatim

from utils.logging import logger

geopy_timeout: int = 10

geolocator = Nominatim(
    user_agent="dating_bot",
    timeout=geopy_timeout,
)


def get_coordinates(city_name: str) -> list | None:
    """Возвращает координаты переданного в city_name города"""
    location = geolocator.geocode(city_name)
    return (location.latitude, location.longitude) if location else None


def get_city_name(latitude: float, longitude: float) -> str | None:
    """Возвращает название города по координатам"""
    try:
        # Обратное геокодирование - получаем адрес по координатам
        location = geolocator.reverse((latitude, longitude), timeout=geopy_timeout)

        if location and location.address:
            # Парсим адрес для извлечения города
            address_parts = location.raw.get("address", {})

            # Ищем город в разных возможных полях
            city = (
                address_parts.get("city")
                or address_parts.get("town")
                or address_parts.get("village")
                or address_parts.get("municipality")
                or address_parts.get("county")
            )

            return city

    except Exception as e:
        logger.error(f"Ошибка получения города: {e}")
        return None


def get_full_address(latitude: float, longitude: float) -> str | None:
    """Возвращает полный адрес по координатам"""
    try:
        location = geolocator.reverse((latitude, longitude), timeout=geopy_timeout)
        return location.address if location else None
    except Exception as e:
        logger.error(f"Ошибка получения адреса: {e}")
        return None
