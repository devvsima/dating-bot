from geopy.distance import geodesic
from geopy.geocoders import Nominatim


def get_coordinates(city_name: str, timeout: int = 10) -> list | None:
    """Возвращает координаты переданного в city_name города"""
    geolocator = Nominatim(user_agent="dating_bot", timeout=timeout)
    location = geolocator.geocode(city_name)
    return (location.latitude, location.longitude) if location else None
