from ..models.users import Users
from utils.misc.logging import logger


def get_user(user_id):
    return Users.select().where(Users.id == user_id)

def get_or_create_user(id: int, username: str = None, language: str = None) -> Users:
    user = get_user(id)

    if user:
        return user

    return create_user(id, username, language)

def create_user(id: int, username: str = None, language: str = None) -> Users:
    logger.info(f"New user {username} | {id}")
    new_user = Users.create(id=id, username=username, language=language)
    return new_user

