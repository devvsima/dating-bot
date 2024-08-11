from ..models.users import Users
from utils.logging import logger


def get_user(id):
    return Users.get(Users.id == id)

def get_or_create_user(id: int, username: str = None, language: str = None) -> Users:
    user = get_user(id)

    if user:
        return user

    return create_user(id, username, language)

def create_user(id: int, username: str = None, language: str = None) -> Users:
    logger.info(f"New user {username} | {id}")
    new_user = Users.create(id=id, username=username, language=language)
    return new_user

def new_referral(id, inviter):
    user = get_user(id)
    print(user)
    print(23123)
    if not user.is_invited:
        Users.update(is_invited = True).where(Users.id == id).execute()
        Users.update(referral=Users.referral + 1).where(Users.id == inviter).execute()

