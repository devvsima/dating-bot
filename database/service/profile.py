from ..models.profile import Profile
from utils.logging import logger

async def get_profile(user_id):
    return Profile.get(Profile.id == user_id)

async def is_profile(user_id):
    return Profile.select().where(Profile.id == user_id).exists()

async def delete_profile(user_id):
    user = await get_profile(user_id)
    user.delete_instance()

async def edit_profile_photo(user_id, photo):
    Profile.update(photo=photo).where(Profile.id == user_id)

async def edit_profile_description(user_id, description):
    Profile.update(description=description).where(Profile.id == user_id)


async def create_profile(state, user_id):
    if await is_profile(user_id):
        await delete_profile(user_id)
        
    async with state.proxy() as data:
        Profile.create(      
            id = user_id,
            gender = data["gender"],
            find_gender = data["find_gender"],
            photo = data["photo"],
            name = data["name"],
            age = data["age"],
            city = data["city"],
            latitude = data["latitude"],
            longitude = data["longitude"],
            description = data["desc"]
            )
    logger.info(f"A new profile has been created from | {user_id}")


from peewee import fn

async def elastic_search_user_ids(user_id, age_range = 3, distance = 0.1):
    user = await get_profile(user_id)
    
    users = Profile.select(Profile.id).where(
        (Profile.active == True) &
        (fn.ABS(Profile.latitude - user.latitude) < distance) &
        (fn.ABS(Profile.longitude - user.longitude) < distance) &
        ((Profile.gender == user.find_gender) | (user.find_gender == 'all')) &  # Учет предпочтений пользователя
        ((user.gender == Profile.find_gender) | (Profile.find_gender == 'all')) &  # Учет предпочтений анкеты
        (Profile.age.between(user.age - age_range, user.age + age_range)) &
        (Profile.id != user_id)
    )
    return [i.id for i in users]