"""
Talia Discord Bot
GNU General Public License v3.0
ping_service.py (Service)

On ping help service
"""
from Utils import guild, message, other


async def run(bot, msg, conn):
    """
    On ping help service runner function, handles the
     message that is sent when Talia is pinged

    1. Loads emojis
    2. Makes sure the channel is valid to send in
    3. Sends the on ping help message
    """
    emojis = other.load_emojis(bot)

    if msg.guild is None:
        try:
            await message.send_message(msg, await message.send_message(msg, f"""I see that you pinged me {emojis.ping}

My prefix is **t!**
You can use `t!help` for some help""", title="Hello!"))
        except TypeError:
            pass

    else:
        guildinfo = guild.load_guild(msg.guild.id, conn)

        if guildinfo is None:
            return

        if msg.channel.id in guildinfo.disabled_channels:
            return

        try:
            await message.send_message(msg, await message.send_message(msg, f"""I see that you pinged me {emojis.ping}

My prefix is **{guildinfo.prefix}**
You can use `{guildinfo.prefix}help` for some help""", title="Hello!"))
        except TypeError:
            pass