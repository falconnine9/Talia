"""
Talia Discord Bot
GNU General Public License v3.0
user.py (Utils)

Utilities for the management of users within the database
"""
import json
from Utils import abc


def load_user(user_id, conn):
    """
    Loads a user from the database

    1. Looks for the user with a certain ID (Based off of discord ID)
    2. Takes the returned list and assigns each value to it's spot in a user object
    3. Attributes stored in a class use the json library for serialization
     and get stored in a dictionary until converted
    """
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users WHERE id = %s", (user_id,))
    userinfo = cur.fetchone()
    
    if userinfo is None:
        return None
    
    new_user = abc.User(userinfo[0])
    new_user.coins = userinfo[1]
    new_user.xp = userinfo[2]
    new_user.level = userinfo[3]
    new_user.edu_level = userinfo[4]
    new_user.multiplier = userinfo[5]
    new_user.company = userinfo[6]
    new_user.hourly = userinfo[7]
    new_user.daily = userinfo[8]
    new_user.partner = userinfo[9]
    new_user.parents = json.loads(userinfo[10])
    new_user.children = json.loads(userinfo[11])

    tmp_settings = json.loads(userinfo[12])
    new_user.settings = abc.Settings(
        tmp_settings["notifs"],
        tmp_settings["timernotifs"],
        tmp_settings["reaction_confirm"]
    )

    new_user.color = json.loads(userinfo[13])
    tmp_shop_info = json.loads(userinfo[14])
    new_user.shop_info = abc.ShopInfo(tmp_shop_info["multiplier_cost"])

    cur.execute("SELECT * FROM job_info WHERE id = %s", (user_id,))
    job_info = cur.fetchone()
    if job_info is None:
        new_user.job = None
    else:
        new_user.job = abc.Job(
            job_info[1], job_info[2], job_info[3],
            json.loads(job_info[4]),
            json.loads(job_info[5])
        )

    cur.execute("SELECT * FROM pickaxe_info WHERE id = %s", (user_id,))
    pickaxe_info = cur.fetchone()
    if pickaxe_info is None:
        new_user.pickaxe = None
    else:
        new_user.pickaxe = abc.Pickaxe(
            pickaxe_info[1], pickaxe_info[2],
            pickaxe_info[3], pickaxe_info[4]
        )

    cur.execute("SELECT * FROM pet_info WHERE id = %s", (user_id,))
    pet_info = cur.fetchone()
    if pet_info is None:
        new_user.pet = None
    else:
        new_user.pet = abc.Pet(
            pet_info[1], pet_info[2],
            pet_info[3], pet_info[4]
        )

    cur.execute("SELECT * FROM items WHERE owner = %s", (user_id,))
    all_items = cur.fetchall()
    new_user.inventory = [
        abc.Item(
            item[2], item[3], item[4],
            json.loads(item[5]), item[0]
        ) for item in all_items
    ]

    cur.execute("SELECT name FROM achievements WHERE owner = %s", (user_id,))
    all_achievements = cur.fetchall()
    new_user.achievements = [achievement[0] for achievement in all_achievements]

    cur.execute("SELECT * FROM showcase_info WHERE id = %s", (user_id,))
    showcase_info = cur.fetchone()
    if showcase_info is None:
        new_user.showcase = None
    else:
        new_user.showcase = abc.Item(
            showcase_info[1], showcase_info[2], showcase_info[3],
            json.loads(showcase_info[4]), None
        )
    
    return new_user


def write_user(obj, conn, write=True):
    """
    Creates a new user entry in the database

    1. Converts all the attributes that should be stored in serialized
     strings to a dictionary instead of a class
    2. Creates a new cursor and inserts the user into the database
    3. Commits if the write parameter is true
    """
    cur = conn.cursor()
    cur.execute(f"INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (
        obj.id,
        obj.coins,
        obj.xp,
        obj.level,
        obj.edu_level,
        obj.multiplier,
        obj.company,
        obj.hourly,
        obj.daily,
        obj.partner,
        json.dumps(obj.parents),
        json.dumps(obj.children),
        json.dumps(obj.settings.cvt_dict()),
        json.dumps(obj.color),
        json.dumps(obj.shop_info.cvt_dict())
    ))

    if write:
        conn.commit()


def set_user_attr(user_id, attr, val, conn, write=True):
    """
    Sets a certain attribute of a user in the database

    1. Checks for the value type and converts it to a value
     that MySQL can understand
    3. Creates a new cursor and sets the value
    4. Commits if the write parameter is true
    """
    if type(val) == list or type(val) == dict:
        val = json.dumps(val)

    cur = conn.cursor()
    cur.execute(f"UPDATE users SET {attr} = %s WHERE id = %s", (val, user_id))

    if write:
        conn.commit()


async def load_user_obj(bot, user_id):
    user_obj = bot.get_user(user_id)

    if user_obj is None:
        return await bot.fetch_user(user_id)
    else:
        return user_obj