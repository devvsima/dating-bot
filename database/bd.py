import sqlite3 as sq
from pathlib import Path


async def db_start():
    global db, cur
    # path = rf"{Path(__file__).parents[0]}\new.db"
    db = sq.connect(rf"{Path(__file__).parents[0]}\database.sqlite")
    cur = db.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS profile(user_id TEXT PRIMARY KEY, gender TEXT, find_gender TEXT ,photo TEXT, name TEXT, age TEXT, city TEXT, desc TEXT)"
    )
    db.commit()


async def create_profile(user_id):
    user = cur.execute(
        "SELECT 1 FROM profile WHERE user_id == '{key}'".format(key=user_id)
    ).fetchone()
    if not user:
        cur.execute(
            "INSERT INTO profile VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
            (user_id, "", "", "", "", "", "", ""),
        )
        db.commit()


async def edit_profile(state, user_id):
    async with state.proxy() as data:
        cur.execute(
            "UPDATE profile SET gender = '{}', find_gender = '{}', photo = '{}', name = '{}', age = '{}', city = '{}', desc = '{}'WHERE user_id == '{}'".format(
                data["gender"],
                data["find_gender"],
                data["photo"],
                data["name"],
                data["age"],
                data["city"],
                data["desc"],
                user_id,
            )
        )
        db.commit()
