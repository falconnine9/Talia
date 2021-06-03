import json

from Utils import abc


def load_guild(guild_id, conn):
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM guilds WHERE id = ?", (guild_id,))
    guildinfo = cur.fetchone()
    
    if guildinfo is None:
        return None
    
    new_guild = abc.Guild(guildinfo[0])
    new_guild.prefix = guildinfo[1]
    new_guild.disabled_channels = json.loads(guildinfo[2])
    
    return new_guild


def write_guild(obj, conn, write=True):
    cur = conn.cursor()
    cur.execute("INSERT INTO guilds VALUES (?, ?, ?)", (
        obj.id,
        obj.prefix,
        json.dumps(obj.disabled_channels)
    ))
    
    if write:
        conn.commit()


def set_guild_attr(guild_id, attr, val, conn, write=True):
    if type(val) == bool:
        val = str(val)
    elif type(val) == list or type(val) == dict:
        val = json.dumps(val)
    
    cur = conn.cursor()
    cur.execute(f"UPDATE guilds SET {attr} = ? WHERE id = ?", (val, guild_id))
    
    if write:
        conn.commit()


def load_guild_prefix(guild_id, conn):
    cur = conn.cursor()
    cur.execute("SELECT prefix FROM guilds WHERE id = ?", (guild_id,))
    guild_prefix = cur.fetchone()

    if guild_prefix is None:
        return "t!"

    return guild_prefix[0]