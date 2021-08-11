from talia.obj.user import User
from talia.util.user_ext.job import get_job, remove_job
from talia.util.user_ext.pickaxe import get_pickaxe, remove_pickaxe


def get_user(id_, guild, cur):
    ui = get_user_base(id_, guild, cur)
    if ui is None:
        return

    ui.job = get_job(ui.id, cur)
    ui.pickaxe = get_pickaxe(ui.id, cur)

    return ui


def get_user_base(id_, guild, cur):
    cur.execute("SELECT * FROM users WHERE user = %s AND guild = %s",
                (id_, guild))
    ui = cur.fetchone()
    if ui is None:
        return None

    return User(
        id=ui[0],
        guild=ui[1],
        user=ui[2],
        pocket=ui[3],
        bank=ui[4],
        level=ui[5],
        xp=ui[6],
        multiplier=ui[7],
        commands=ui[8],
        job=None,
        pickaxe=None,
        partner=None,
        parents=set(),
        children=set()
    )


def new_user(obj, cur):
    cur.execute("INSERT INTO users (guild, user, pocket,"
                "bank, level, xp, multiplier, commands) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (obj.guild,
                 obj.user,
                 obj.pocket,
                 obj.bank,
                 obj.level,
                 obj.xp,
                 obj.multiplier,
                 obj.commands))


def remove_user(id_, cur):
    cur.execute("DELETE FROM users WHERE id = %s", (id_,))
    remove_job(id_, cur)
    remove_pickaxe(id_, cur)


def get_uid(id_, guild, cur):
    cur.execute("SELECT id FROM users WHERE user = %s AND guild = %s",
                (id_, guild))
    uid = cur.fetchone()
    return None if uid is None else uid[0]