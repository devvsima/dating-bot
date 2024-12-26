from ..models.likes import Likes

from utils.logging import logger



def set_new_like(liker_id: int, liked_id: int) -> None:
    """Добавляет в БД лайк пользователя liker_id к пользователю liked_id, если лайк уже есть - ничего не делает"""
    existing_like = Likes.get_or_none(liker_id=liker_id, liked_id=liked_id)

    if existing_like is None:
        logger.info(f"User: {liker_id} | лайкнул пользователя {liked_id}")
        
        Likes.create(liker_id=liker_id, liked_id=liked_id)
    else:
        logger.info(f"Повторился лайк: {liker_id} - {liked_id}")
    
def get_profile_likes(user_id: int) -> list:
    ids = Likes.select(Likes).where(Likes.liked_id == user_id)
    return [i.liker_id for i in ids]

def del_like(liked_id: int, liker_id: int) -> None:
    """Удаляет из БД лайк пользователя liker_id к пользователю liked_id"""
    logger.info(f"{liker_id} лайкнул {liked_id} | лайк удален")
    Likes.delete().where((Likes.liker_id == liker_id) & (Likes.liked_id == liked_id)).execute()

