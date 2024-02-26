from ..models.profile import Profile
from utils.misc.logging import logger



async def get_profile(user_id):
    return Profile.get(Profile.id == user_id)

async def if_profile(user_id):
    return Profile.select().where(Profile.id == user_id).exists()

async def delete_profile(user_id):
    user = await get_profile(user_id)
    user.delete_instance()

async def edit_profile_photo(user_id, photo):
    Profile.update(photo=photo).where(Profile.id == user_id)

async def edit_profile_description(user_id, description):
    Profile.update(description=description).where(Profile.id == user_id)


async def create_profile(state, user_id):
    async with state.proxy() as data:
        Profile.create(      
            id = user_id,
            gender = data["gender"],
            find_gender = data["find_gender"],
            photo = data["photo"],
            name = data["name"],
            age = data["age"],
            city = data["city"],
            description = data["desc"]
            )


async def elastic_search_user_ids(user_id):
    user = await get_profile(user_id)
    users = Profile.select(Profile.id).where((Profile.city == user.city) & (Profile.id != user_id))
    return [i.id for i in users]

