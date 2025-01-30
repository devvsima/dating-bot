from ..models.users import Users
from utils.logging import logger


async def get_user(user_id: int) -> Users | None:
    """Возвращает пользователя по его id"""
    try:
        return Users.get(Users.id == user_id)
    except:
        return None


async def get_or_create_user(user_id: int, username: str = None, language: str = None) -> Users:
    """Возвращает пользователя по его id, если его нет - создает"""
    if user := await get_user(user_id):
        return user

    return await create_user(user_id, username, language)


async def create_user(user_id: int, username: str = None, language: str = None) -> Users:
    """Создает нового пользователя"""
    logger.info(f"New user: {user_id} | {username}")
    return Users.create(id=user_id, username=username, language=language)


async def update_user_username(user_id: int, username: str = None) -> None:
    """Обновляет данные пользователя"""
    Users.update(username=username).where(Users.id == user_id).execute()
    logger.info(f"Update user: {user_id} | {username}")


async def new_referral(inviter_id: int) -> None:
    """Добавляет приведенного реферала к пользователю inviter_id"""
    Users.update(referral=Users.referral + 1).where(Users.id == inviter_id).execute()
    logger.info(f"User: {inviter_id} | привел нового пользователя")

    
async def change_language(user_id: int, language: str) -> None:
    """Изменяет язык пользователя на language"""
    Users.update(language=language).where(Users.id == user_id).execute()
    logger.info(f"User: {user_id} | изменил язык на - {language}")

    
async def toggle_user_ban(user: Users) -> None:
    """Меняет статус блокировки пользователя на противоположный"""
    user.is_banned = not user.is_banned
    user.save()


async def ban_or_unban_user(user_id: int, is_banned: bool) -> None:
    """Меняет статус блокировки пользователя на заданный"""
    Users.update(is_banned=is_banned).where(Users.id == user_id).execute()
    logger.info(f"User: {user_id} | стату блокироваки изминен на - {is_banned}")
