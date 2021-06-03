import json

from Utils import abc


def load_user(user_id, conn):
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users WHERE id = ?", (user_id,))
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
            tmp_pickaxe["xp"],
            tmp_pickaxe["level"],
            tmp_pickaxe["speed"],
            tmp_pickaxe["multiplier"]
        )

    new_user.achievements = json.loads(userinfo[7])
    new_user.inventory = [abc.Item(
        item["name"], item["worth"],
        item["type"], item["stats"]
    ) for item in json.loads(userinfo[8])]
    new_user.fusion_level = userinfo[9]
    new_user.multiplier = userinfo[10]
    new_user.company = userinfo[11]

    tmp_showcase = json.loads(userinfo[12])
    if tmp_showcase["name"] is None:
        new_user.showcase = None
    else:
        new_user.showcase = abc.Item(
            tmp_showcase["name"],
            tmp_showcase["worth"],
            tmp_showcase["type"],
            tmp_showcase["stats"]
        )
    
    return new_user


def write_user(obj, conn, write=True):
    if obj.job is None:
        tmp_job = {"name": None, "xp": 0, "level": 1, "salary": [], "cooldown": []}
    else:
        tmp_job = obj.job.cvt_dict()

    if obj.pickaxe is None:
        tmp_pickaxe = {"name": None, "worth": 0, "xp": 0, "level": 1, "speed": 1, "multiplier": 1.0}
    else:
        tmp_pickaxe = obj.pickaxe.cvt_dict()

    if obj.showcase is None:
        tmp_showcase = {"name": None, "worth": 0, "type": "box_item", "stats": {}}
    else:
        tmp_showcase = obj.showcase.cvt_dict()

    cur = conn.cursor()
    cur.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
        obj.id,
        obj.coins,
        obj.xp,
        obj.level,
        obj.edu_level,
        json.dumps(tmp_job),
        json.dumps(tmp_pickaxe),
        json.dumps(obj.achievements),
        json.dumps([item.cvt_dict() for item in obj.inventory]),
        obj.fusion_level,
        obj.multiplier,
        obj.company,
        json.dumps(tmp_showcase)
    ))
    
    if write:
        conn.commit()


def set_user_attr(user_id, attr, val, conn, write=True):
    if attr == "inventory":
        val = json.dumps([item.cvt_dict() for item in val])
    else:
        if type(val) == bool:
            val = str(val)
        elif type(val) == list or type(val) == dict:
            val = json.dumps(val)
    
    cur = conn.cursor()
    cur.execute(f"UPDATE users SET {attr} = ? WHERE id = ?", (val, user_id))
    
    if write:
        conn.commit()