"""
Talia Discord Bot
GNU General Public License v3.0
user.py (Utils)

Utilities for the management of users within the database
"""
import asyncio
import concurrent.futures
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

    tmp_job = json.loads(userinfo[5])
    if tmp_job["name"] is None:
        new_user.job = None
    else:
        new_user.job = abc.Job(
            tmp_job["name"],
            tmp_job["xp"],
            tmp_job["level"],
            tmp_job["salary"],
            tmp_job["cooldown"]
        )

    tmp_pickaxe = json.loads(userinfo[6])
    if tmp_pickaxe["name"] is None:
        new_user.pickaxe = None
    else:
        new_user.pickaxe = abc.Pickaxe(
            tmp_pickaxe["name"],
            tmp_pickaxe["worth"],
            tmp_pickaxe["speed"],
            tmp_pickaxe["multiplier"]
        )

    tmp_pet = json.loads(userinfo[7])
    if tmp_pet["name"] is None:
        new_user.pet = None
    else:
        new_user.pet = abc.Pet(
            tmp_pet["name"],
            tmp_pet["worth"],
            tmp_pet["type"],
            tmp_pet["breed"]
        )

    new_user.achievements = json.loads(userinfo[8])
    new_user.inventory = [abc.Item(
        item["name"], item["worth"],
        item["type"], item["stats"]
    ) for item in json.loads(userinfo[9])]
    new_user.fusion_level = userinfo[10]
    new_user.multiplier = userinfo[11]
    new_user.company = userinfo[12]

    tmp_showcase = json.loads(userinfo[13])
    if tmp_showcase["name"] is None:
        new_user.showcase = None
    else:
        new_user.showcase = abc.Item(
            tmp_showcase["name"],
            tmp_showcase["worth"],
            tmp_showcase["type"],
            tmp_showcase["stats"]
        )

    new_user.hourly = userinfo[14]
    new_user.daily = userinfo[15]
    new_user.partner = userinfo[16]
    new_user.parents = json.loads(userinfo[17])
    new_user.children = json.loads(userinfo[18])

    tmp_settings = json.loads(userinfo[19])
    new_user.settings = abc.Settings(
        tmp_settings["notifs"],
        tmp_settings["timernotifs"],
        tmp_settings["reaction_confirm"]
    )

    new_user.color = json.loads(userinfo[20])
    
    return new_user


def write_user(obj, conn, write=True):
    """
    Creates a new user entry in the database

    1. Converts all the attributes that should be stored in serialized
     strings to a dictionary instead of a class
    2. Creates a new cursor and inserts the user into the database
    3. Commits if the write parameter is true
    """
    if obj.job is None:
        tmp_job = {"name": None, "xp": 0, "level": 1, "salary": [], "cooldown": []}
    else:
        tmp_job = obj.job.cvt_dict()

    if obj.pickaxe is None:
        tmp_pickaxe = {"name": None, "worth": 0, "speed": 1, "multiplier": 1.0}
    else:
        tmp_pickaxe = obj.pickaxe.cvt_dict()

    if obj.pet is None:
        tmp_pet = {"name": None, "worth": 0, "type": None, "breed": None}
    else:
        tmp_pet = obj.pet.cvt_dict()

    if obj.showcase is None:
        tmp_showcase = {"name": None, "worth": 0, "type": "box_item", "stats": {}}
    else:
        tmp_showcase = obj.showcase.cvt_dict()

    cur = conn.cursor()
    cur.execute(f"INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (
        obj.id,
        obj.coins,
        obj.xp,
        obj.level,
        obj.edu_level,
        json.dumps(tmp_job),
        json.dumps(tmp_pickaxe),
        json.dumps(tmp_pet),
        json.dumps(obj.achievements),
        json.dumps([item.cvt_dict() for item in obj.inventory]),
        obj.fusion_level,
        obj.multiplier,
        obj.company,
        json.dumps(tmp_showcase),
        obj.hourly,
        obj.daily,
        obj.partner,
        json.dumps(obj.parents),
        json.dumps(obj.children),
        json.dumps(obj.settings.cvt_dict()),
        json.dumps(obj.color)
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
    if attr == "inventory":
        val = json.dumps([item.cvt_dict() for item in val])
    else:
        if type(val) == bool:
            val = str(val)
        elif type(val) == list or type(val) == dict:
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