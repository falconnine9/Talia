from talia.obj.pickaxe import GuildPickaxe


def get_all_pickaxes(id_, cur):
    cur.execute("SELECT * FROM g_picks WHERE guild = %s", (id_,))
    return {GuildPickaxe(
        pickaxe_id=pi[0],
        guild=pi[1],
        name=pi[2],
        cost=pi[3],
        speed=pi[4],
        multi=pi[5]
    ) for pi in cur.fetchall()}


def new_pickaxe(obj, cur):
    cur.execute(("INSERT INTO g_picks (guild, name,"
                 "cost, speed, multi) "
                 "VALUES (%s, %s, %s, %s, %s)"),
                (obj.guild,
                 obj.name,
                 obj.cost,
                 obj.speed,
                 obj.multi))


def remove_pickaxe(pickaxe_id, cur):
    cur.execute("DELETE FROM g_picks WHERE pickaxe_id = %s", (pickaxe_id,))


def remove_all_pickaxes(id_, cur):
    cur.execute("DELETE FROM g_picks WHERE guild = %s", (id_,))