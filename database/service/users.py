# from ..connect import db_users


async def add_user(user_id):
    Users.create(id=user_id)


async def find_user(user_id):
    return Users.select().where(Users.id == user_id)


async def delete_profile(user_id):
    pass
    # db_users.find_one_and_delete({"_id": user_id})


# async def set(user_id=int, what=str, text=str):
#     db_users.update_one({"_id": user_id}, {"$set": {what: text}})


async def get_profile(user_id):
    return Users.get(Users.id == user_id)


async def find_user_id(user_id):
    user_profile = await find_user(user_id)

    filter_condition = {"city": f"{user_profile['city']}", "_id": {"$ne": user_id}}
    # cursor = db_users.find(filter_condition)

    # user_ids = [doc["_id"] for doc in cursor]
    # return user_ids

from ..models.users import Users

async def edit_profile(state, user_id):
    async with state.proxy() as data:
        Users.create(      
            id = user_id,
            gender = data["gender"],
            find_gender = data["find_gender"],
            photo = data["photo"],
            name = data["name"],
            age = data["age"],
            city = data["city"],
            description = data["desc"]
            )