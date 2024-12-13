from ..models.users import Users
from utils.logging import logger


def get_user(id) -> Users:
    try:
        return Users.get(Users.id == id)
    except:
        return None

def get_or_create_user(id: int, username: str = None, language: str = None) -> Users:
    user = get_user(id)

    if user:
        return user

    return create_user(id, username, language)

def create_user(id: int, username: str = None, language: str = None) -> Users:
    logger.info(f"New user: {id} | {username}")
    new_user = Users.create(id=id, username=username, language=language)
    return new_user

def new_referral(inviter) -> None:
    Users.update(referral=Users.referral + 1).where(Users.id == inviter).execute()
    logger.info(f"User: {inviter} | привел нового пользователя")
    
def change_language(id: int, language: str):
    Users.update(language=language).where(Users.id == id).execute()
