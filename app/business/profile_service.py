from database.models.profile import ProfileModel
from database.models.user import UserModel
from database.services.search import haversine_distance
from loader import bot


async def send_profile(chat_id: int, profile: ProfileModel) -> None:
    """Отправляет пользователю переданный в функцию профиль"""
    await bot.send_photo(
        chat_id=chat_id,
        photo=profile.photo,
        caption=f"{profile.name}, {profile.age}, {profile.city}\n{profile.description}",
        parse_mode=None,
    )


async def send_profile_with_dist(user: UserModel, profile: ProfileModel, keyboard=None) -> None:
    """Отправляет профиль пользователя с расстоянием до него в киломтерах"""
    if profile.city == "📍":
        distance = haversine_distance(
            user.profile.latitude, user.profile.longitude, profile.latitude, profile.longitude
        )
        city = f"📍 {round(distance, 2)} km"
    else:
        city = profile.city
    await bot.send_photo(
        chat_id=user.id,
        photo=profile.photo,
        caption=f"{profile.name}, {profile.age}, {city}\n{profile.description}",
        reply_markup=keyboard,
        parse_mode=None,
    )
