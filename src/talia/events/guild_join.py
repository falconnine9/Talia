from main import client
from talia.const import DEFAULT_PREFIX, URL
from talia.obj.guild import Guild
from talia.util.console import log
from talia.util.guild import new_guild
from talia.util.message import send_embed


@client.event
async def on_guild_join(guild):
    log(f"Added to guild {guild.name}#{guild.id}")
    new_guild(Guild.default(), client.conn.cursor())

    if (guild.system_channel is not None and
            guild.system_channel.permissions_for(guild.me).send_messages):
        await send_embed(
            None, guild.system_channel,
            desc=("You can check out my list of commands with "
                  f"`{DEFAULT_PREFIX}help`\n"
                  f"Or change up some of my settings on my [dashboard]({URL}"),
            title="Thanks for adding me to your server"
        )