def get_all_dc(id_, cur):
    cur.execute("SELECT channel FROM dc WHERE guild = %s", (id_,))
    return {channel[0] for channel in cur.fetchall()}


def new_dc(channel, guild, cur):
    cur.execute("INSERT INTO dc VALUES (%s, %s)", (channel, guild))


def remove_dc(channel, cur):
    cur.execute("DELETE FROM dc WHERE channel = %s", (channel,))


def remove_all_dc(id_, cur):
    cur.execute("DELETE FROM dc WHERE guild = %s", (id_,))