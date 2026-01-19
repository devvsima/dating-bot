"""
API endpoints для администраторов
"""

from fastapi import APIRouter, HTTPException, Request

from api.models import ProfileResponse
from data.config import tgbot
from database.connect import get_session
from database.services.profile_media import ProfileMedia
from database.services.user import User
from utils.telegram_requests import get_photo_url_by_file_id

router = APIRouter()


def check_admin(request: Request) -> int:
    """
    Проверка прав администратора через Telegram WebApp initData

    Args:
        request: HTTP запрос

    Returns:
        ID администратора

    Raises:
        HTTPException: Если пользователь не администратор
    """
    # Получаем данные из Telegram WebApp
    # В реальном приложении здесь нужно парсить initData из заголовка
    # Для примера используем query параметр admin_id
    admin_id = request.query_params.get("admin_id")

    if not admin_id:
        raise HTTPException(status_code=403, detail="Требуется авторизация")

    try:
        admin_id = int(admin_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Неверный формат admin_id")

    if admin_id not in tgbot.ADMINS:
        raise HTTPException(status_code=403, detail="Доступ запрещен")

    return admin_id


@router.get("/admin/user/{user_id}", response_model=ProfileResponse)
async def get_user_profile(user_id: int, request: Request):
    """
    Получение профиля пользователя для администратора

    Args:
        user_id: ID пользователя для просмотра
        request: HTTP запрос (для проверки прав администратора)

    Returns:
        JSON с данными профиля пользователя
    """
    # Проверяем права администратора
    admin_id = check_admin(request)

    async with get_session() as session:
        # Получаем пользователя с профилем
        user = await User.get_with_profile(session=session, id=user_id)

        if not user or not user.profile:
            raise HTTPException(status_code=404, detail="Профиль не найден")

        # Получаем все фото из медиа
        photos = []
        media_items = await ProfileMedia.get_profile_photos(
            session=session, profile_id=user.profile.id
        )
        for item in media_items:
            photos.append(get_photo_url_by_file_id(item.media))

        # Возвращаем данные профиля
        return ProfileResponse(
            id=user.id,
            username=user.username,
            name=user.profile.name,
            age=user.profile.age,
            gender=user.profile.gender,
            city=user.profile.city,
            description=user.profile.description,
            instagram=user.profile.instagram,
            photos=photos,
        )
