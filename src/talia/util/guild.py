from bot import client
from talia.const import DEFAULT_PREFIX
from talia.obj.guild import Guild
from talia.util.guild_ext.dc import get_all_dc, remove_all_dc
from talia.util.guild_ext.dco import get_all_dco, remove_all_dco
from talia.util.guild_ext.ds import get_all_ds, remove_all_ds
from talia.util.guild_ext.job import get_all_jobs, remove_all_jobs
from talia.util.guild_ext.pickaxe import get_all_pickaxes, remove_all_pickaxes


def get_guild(id_, cur):
    gi = get_guild_base(id_, cur)
    if gi is None:
        return None

    gi.dc = get_all_dc(id_, cur)
    gi.dco = get_all_dco(id_, cur)
    gi.ds = get_all_ds(id_, cur)
    gi.jobs = get_all_jobs(id_, cur)
    gi.pickaxes = get_all_pickaxes(id_, cur)

    return gi


def get_guild_base(id_, cur):
    cur.execute("SELECT * FROM guilds WHERE id = %s", (id_,))
    gi = cur.fetchone()
    if gi is None:
        return None

    return Guild(
        id=gi[0],
        prefix=gi[1],
        ud_mode=gi[2],
        start_coins=gi[3],
        dc=set(),
        dco=set(),
        ds=set(),
        jobs=set(),
        pickaxes=set()
    )


def new_guild(obj, cur):
    cur.execute("INSERT INTO guilds VALUES (%s, %s, %s, %s)",
                (obj.id,
                 obj.prefix,
                 obj.ud_mode,
                 obj.start_coins))


def remove_guild(id_, cur, full_delete=True):
    cur.execute("DELETE FROM guilds WHERE id = %s", (id_,))

    if full_delete:
        cur.execute("DELETE FROM users WHERE guild = %s", (id_,))
        remove_all_dc(id_, cur)
        remove_all_dco(id_, cur)
        remove_all_ds(id_, cur)
        remove_all_jobs(id_, cur)
        remove_all_pickaxes(id_, cur)

        cur.execute(("DELETE FROM u_jobs WHERE user IN "
                     "(SELECT id FROM users WHERE guild = %s)"), (id_,))
        cur.execute(("DELETE FROM u_picks WHERE user IN"
                     "(SELECT id FROM users WHERE guild = %s)"), (id_,))
        cur.execute(("DELETE FROM relations WHERE user IN "
                     "(SELECT id FROM users WHERE guild = %s)"), (id_,))


def get_prefix(id_, conn=None, confirm=False):
    try:
        return client.prefixes[id_]
    except KeyError:
        if confirm and conn is not None:
            cur = conn.cursor()
            cur.execute("SELECT prefix FROM guilds WHERE id = %s", (id_,))
            prefix = cur.fetchone()
            if prefix is None:
                client.prefixes[id_] = DEFAULT_PREFIX
                return DEFAULT_PREFIX
            else:
                client.prefixes[id_] = prefix[0]
                return prefix[0]