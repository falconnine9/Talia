"""
Talia Discord Bot
GNU General Public License v3.0
channels.py (Commands/Settings)

channels command
"""
from Utils import guild, message, other
from Storage import help_list

name = "channels"
dm_capable = False


async def run(args, bot, msg, conn):
    if not msg.author.guild_permissions.manage_channels and msg.author.id not in other.load_config().owners:
        await message.send_error(msg, "You have insufficient permissions to use this command")
        return

    if len(args) < 2:
        await message.invalid_use(msg, help_list.channels, "No operation given")
        return

    if len(args) < 3:
        await message.invalid_use(msg, help_list.channels, "No channel given")
        return

    args[1] = args[1].lower()

    if args[1] == "enable":
        await _channels_enable(msg, conn, args)
    elif args[1] == "disable":
        await _channels_disable(msg, conn, args)
    else:
        await message.send_error(msg, f"Unknown operation: {args[1]}")


async def _channels_enable(msg, conn, args):
    args[2] = args[2].replace("<#", "").replace(">", "")

    try:
        channel = msg.guild.get_channel(int(args[2]))
    except ValueError:
        await message.send_error(msg, "Invalid channel")
        return

    if channel is None:
        await message.send_error(msg, "I can't find that channel")
        return

    guildinfo = guild.load_guild(msg.guild.id, conn)

    if channel.id not in guildinfo.disabled_channels:
        await message.send_error(msg, f"{channel.mention} is already enabled")
        return

    guildinfo.disabled_channels.remove(channel.id)
    guild.set_guild_attr(msg.guild.id, "disabled_channels", guildinfo.disabled_channels, conn)

    await message.send_message(msg, f"{channel.mention} has been enabled")


async def _channels_disable(msg, conn, args):
    args[2] = args[2].replace("<#", "").replace(">", "")

    try:
        channel = msg.guild.get_channel(int(args[2]))
    except ValueError:
        await message.send_error(msg, "Invalid channel")
        return

    if channel is None:
        await message.send_error(msg, "I can't find that channel")
        return

    guildinfo = guild.load_guild(msg.guild.id, conn)

    if channel.id in guildinfo.disabled_channels:
        await message.send_error(msg, f"{channel.mention} is already disabled")
        return

    guildinfo.disabled_channels.append(channel.id)
    guild.set_guild_attr(msg.guild.id, "disabled_channels", guildinfo.disabled_channels, conn)

    await message.send_message(msg, f"{channel.mention} has been disabled")