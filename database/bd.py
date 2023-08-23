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


def view_profile(user_id):
    info = cur.execute(
        f"""SELECT * FROM profile
            WHERE user_id = {user_id};
    """
    ).fetchone()
    db.commit()
    return info


def search_profile(user_id):
    ret = cur.execute(
        f"""SELECT * FROM profile WHERE city LIKE '%{view_profile(user_id)[6]}%'"""
    ).fetchall()
    db.commit()
    return ret


def get_user_id(user_id):
    all_us_id = cur.execute(
        f"SELECT user_id FROM profile WHERE user_id LIKE '%{user_id}%'"
    ).fetchone()
    db.commit()
    return all_us_id


# ('743347029', 'Я парень', 'Девушки', 'AgACAgIAAxkBAAIEtmTh4Me_AAEQOyyWxS13tiWyI3hojAACussxG5agEEtpBoZ7y3UZvAEAAwIAA3MAAzAE', 'fff', '19', 'Київ', 'vfr')
