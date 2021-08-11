def get_all_dco(id_, cur):
    cur.execute("SELECT command FROM dco WHERE guild = %s", (id_,))
    return {command[0] for command in cur.fetchall()}


def new_dco(command, guild, cur):
    cur.execute("INSERT INTO dco (guild, command) VALUES (%s, %s)",
                (guild, command))


def remove_dco(command, guild, cur):
    cur.execute("DELETE FROM dco WHERE command = %s and guild = %s",
                (command, guild))


def remove_all_dco(id_, cur):
    cur.execute("DELETE FROM dco WHERE guild = %s", (id_,))