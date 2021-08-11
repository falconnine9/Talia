from talia.obj.job import UserJob


def get_job(id_, cur):
    cur.execute("SELECT * FROM u_jobs WHERE user = %s", (id_,))
    ji = cur.fetchone()
    if ji is None:
        return None

    return UserJob(
        user=ji[0],
        name=ji[1],
        s_min=ji[2],
        s_max=ji[3],
        c_min=ji[4],
        c_max=ji[5],
        level=ji[6],
        xp=ji[7]
    )


def new_job(obj, cur):
    cur.execute("INSERT INTO u_jobs VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (obj.user,
                 obj.name,
                 obj.s_min,
                 obj.s_max,
                 obj.c_min,
                 obj.c_max,
                 obj.level,
                 obj.xp))


def remove_job(id_, cur):
    cur.execute("DELETE FROM u_jobs WHERE user = %s", (id_,))