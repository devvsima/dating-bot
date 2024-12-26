from ..models.users import Users
from utils.logging import logger


def get_user(user_id: int) -> Users or None:
    """Возвращает пользователя по его id"""
    try:
        return Users.get(Users.id == user_id)
    except:
        return None

def get_or_create_user(user_id: int, username: str = None, language: str = None) -> Users:
    """Возвращает пользователя по его id, если его нет - создает"""
    user = get_user(user_id)

    if user:
        return user

    return create_user(user_id, username, language)

def create_user(user_id: int, username: str = None, language: str = None) -> Users:
    """Создает нового пользователя"""
    logger.info(f"New user: {user_id} | {username}")
    new_user = Users.create(id=user_id, username=username, language=language)
    return new_user

def new_referral(inviter_id: int) -> None:
    """Добавляет приведенного реферала к пользователю inviter_id"""
    Users.update(referral=Users.referral + 1).where(Users.id == inviter_id).execute()
    logger.info(f"User: {inviter_id} | привел нового пользователя")
    
def change_language(user_id: int, language: str):
    """Изменяет язык пользователя на language"""
    Users.update(language=language).where(Users.id == user_id).execute()
