from talia.obj.job import GuildJob


def get_all_jobs(id_, cur):
    cur.execute("SELECT * FROM g_jobs WHERE guild = %s", (id_,))
    return {GuildJob(
        job_id=ji[0],
        guild=ji[1],
        name=ji[2],
        s_min=ji[3],
        s_max=ji[4],
        c_min=ji[5],
        c_max=ji[6]
    ) for ji in cur.fetchall()}


def new_job(obj, cur):
    cur.execute(("INSERT INTO g_jobs (guild, name,"
                 "s_min, s_max, c_min, c_max) "
                 "VALUES (%s, %s, %s, %s, %s, %s)"),
                (obj.guild,
                 obj.name,
                 obj.s_min,
                 obj.s_max,
                 obj.c_min,
                 obj.c_max))


def remove_job(job_id, cur):
    cur.execute("DELETE FROM g_jobs WHERE job_id = %s", (job_id,))


def remove_all_jobs(id_, cur):
    cur.execute("DELETE FROM g_jobs WHERE guild = %s", (id_,))