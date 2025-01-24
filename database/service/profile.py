from ..models.profile import Profile

from utils.logging import logger


async def get_profile(user_id: int):
    """Возвращает профиль пользователя"""
    return Profile.get_or_none(Profile.user_id == user_id)

async def delete_profile(user_id: int):
    """Удаляет профиль пользователя"""
    user = await get_profile(user_id)
    user.delete_instance()
    logger.info(f"User: {user_id} | удалил профиль")
    
async def edit_profile_photo(user_id, photo):
    """Изменяет фотографию пользователя"""
    Profile.update(photo=photo).where(Profile.user_id == user_id).execute()
    logger.info(f"User: {user_id} | изменил фотографию")
    
async def edit_profile_description(user_id, description):
    """Изменяет описание пользователя"""
    Profile.update(description=description).where(Profile.user_id == user_id).execute()
    logger.info(f"User | {user_id} изменил описание")

async def create_profile(data, user_id):
    """Создает профиль пользователя, если профиль есть - удаляет его"""
    if await get_profile(user_id):
        await delete_profile(user_id)
        
    Profile.create(      
        user_id = user_id,
        gender = data.get("gender"),
        find_gender = data.get("find_gender"),
        photo = data.get("photo"),
        name = data.get("name"),
        age = data.get("age"),
        city = data.get("city"),
        latitude = data.get("latitude"),
        longitude = data.get("longitude"),
        description = data.get("desc")
    )
    logger.info(f"User: {user_id} | создал анкету")
    
