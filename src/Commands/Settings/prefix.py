"""
Talia Discord Bot
GNU General Public License v3.0
prefix.py (Commands/Settings)

prefix command
"""
import os
from Utils import guild, message, other
from Storage import help_list

#   Command Information   #
name = "prefix"
dm_capable = False
# ~~~~~~~~~~~~~~~~~~~~~~~ #


async def run(bot, msg, conn):
    if not msg.author.guild_permissions.manage_guild and msg.author.id not in other.load_config().owners:
        await message.send_error(msg, "You have insufficient permissions to use this command")
        return

    split_data = msg.content.split(" ")

    if len(split_data) < 2:
        await message.invalid_use(msg, help_list.prefix, "No new prefix given")
        return

    new_prefix = " ".join(split_data[1:])

    if len(new_prefix) > 64:
        await message.send_error(msg, "The prefix can't be longer than 64 characters")
        return

    for char in new_prefix:
        if ord(char) < 32 or ord(char) > 126:
            await message.send_error(msg, f"Invalid character: {char}")
            return

    guildinfo = guild.load_guild(msg.guild.id, conn)

    if guildinfo.prefix == new_prefix:
        await message.send_error(msg, f"The server prefix is already {new_prefix}")
        return

    guild.set_guild_attr(msg.guild.id, "prefix", new_prefix, conn)
    os.environ[f"TaliaPrefix.{msg.guild.id}"] = new_prefix

    await message.send_message(msg, f"Prefix set to: {new_prefix}", title="New prefix")