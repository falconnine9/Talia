from talia.obj.pickaxe import UserPickaxe


def get_pickaxe(id_, cur):
    cur.execute("SELECT * FROM u_picks WHERE user = %s", (id_,))
    pi = cur.fetchone()
    if pi is None:
        return None

    return UserPickaxe(
        user=pi[0],
        name=pi[1],
        worth=pi[2],
        speed=pi[3],
        multi=pi[4]
    )


def new_pickaxe(obj, cur):
    cur.execute("INSERT INTO u_jobs VALUES (%s, %s, %s, %s, %s)",
                (obj.user,
                 obj.name,
                 obj.worth,
                 obj.speed,
                 obj.multi))


def remove_pickaxe(id_, cur):
    cur.execute("DELETE FROM u_picks WHERE user = %s", (id_,))