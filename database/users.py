from .connect import db_users


async def add_user(user_id):
    db_users.update_one({"$set":{"_id": user_id}})
    
async def find_user(user_id):
    a = db_users.find_one({"_id": user_id})
    return a

async def delete_profile(user_id):
    db_users.find_one_and_delete({"_id": user_id})


async def set(user_id=int, what=str, text=str):
    db_users.update_one({"_id": user_id}, {"$set": {what: text}})


async def get_profile(user_id):
    user_profile = db_users.find_one({"_id": user_id}, {"_id": 0})
    return user_profile

async def find(user_id):
    user_profile = db_users.find_one({"_id": user_id}, {"_id": 0})
    users_id = db_users.find(
        {
            "$and": [
                {
                    "_id": {"$not": user_id},
                    "city": user_profile["city"],
                    "gender": user_profile["find_gender"],
                }
            ]
        },
        {"_id": 1},
    )
    print(users_id)
    return users_id


async def edit_profile(state, user_id):
    async with state.proxy() as data:
        db_users.update_one(
            {"_id": user_id},
            {
                "$set": {
                    "gender": data["gender"],
                    "find_gender": data["find_gender"],
                    "photo": data["photo"],
                    "name": data["name"],
                    "age": data["age"],
                    "city": data["city"],
                    "description": data["desc"],
                }
            },
        )

        # cur.execute(
        #     "UPDATE profile SET gender = '{}', find_gender = '{}', photo = '{}', name = '{}', age = '{}', city = '{}', desc = '{}'WHERE user_id == '{}'".format(
        #         data["gender"],
        #         data["find_gender"],
        #         data["photo"],
        #         data["name"],
        #         data["age"],
        #         data["city"],
        #         data["desc"],
        #         user_id,
        #     )
        # )
        # db.commit()
