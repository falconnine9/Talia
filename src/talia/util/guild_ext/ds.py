def get_all_ds(id_, cur):
    cur.execute("SELECT service FROM ds WHERE guild = %s", (id_,))
    return {service[0] for service in cur.fetchall()}


def new_ds(service, guild, cur):
    cur.execute("INSERT INTO guilds (guild, service) VALUES (%s, %s)",
                (guild, service))


def remove_ds(service, guild, cur):
    cur.execute("DELETE FROM ds WHERE service = %s AND guild = %s",
                (service, guild))


def remove_all_ds(id_, cur):
    cur.execute("DELETE FROM ds WHERE guild = %s", (id_,))