from main import client
from talia.util.console import log
from talia.util.guild import remove_guild


@client.event
async def on_guild_remove(guild):
    log(f"Removed from guild {guild.name}#{guild.id}")
    remove_guild(guild.id, client.conn.cursor(), full_delete=True)