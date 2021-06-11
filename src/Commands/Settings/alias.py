"""
Talia Discord Bot
GNU General Public License v3.0
alias.py (Commands/Settings)

alias command
"""
import asyncio
from Utils import guild, message, other
from Storage import help_list


async def run(bot, msg, conn):
    if not msg.author.guild_permissions.manage_guild and msg.author.id not in other.load_config().owners:
        await message.send_error(msg, "You have insufficient permissions to use this command")
        return

    split_data = msg.content.split(" ")

    if len(split_data) < 2:
        await message.invalid_use(msg, help_list.alias, "No operation given")
        return

    split_data[1] = split_data[1].lower()

    if split_data[1] == "create":
        await _alias_create(msg, conn, split_data)

    elif split_data[1] == "remove":
        await _alias_remove(msg, conn, split_data)

    elif split_data[1] == "clear":
        await _alias_clear(bot, msg, conn)

    elif split_data[1] == "list":
        await _alias_list(msg, conn)

    else:
        await message.send_error(msg, f"Unknown operation: {split_data[1]}")


async def _alias_create(msg, conn, split_data):
    if len(split_data) < 3:
        await message.invalid_use(msg, help_list.alias, "No alias given")
        return

    if len(split_data) < 4:
        await message.invalid_use(msg, help_list.alias, "No command given")
        return

    split_data[2] = split_data[2].lower()
    split_data[3] = split_data[3].lower()

    if len(split_data[2]) > 64:
        await message.send_error(msg, "The alias must be less than 64 characters long")
        return

    for char in split_data[2]:
        if ord(char) < 32 or ord(char) > 126:
            await message.send_error(msg, f"Invalid character: {char}")
            return

    if len(split_data[3]) > 64:
        await message.send_error(msg, "The command must be less than 64 characters long")
        return

    for char in split_data[3]:
        if ord(char) < 32 or ord(char) > 126:
            await message.send_error(msg, f"Invalid character: {char}")
            return

    guildinfo = guild.load_guild(msg.guild.id, conn)

    if split_data[2] in guildinfo.aliases.keys():
        await message.send_error(msg, "An alias with that name already exists")
        return

    guildinfo.aliases[split_data[2]] = split_data[3]
    guild.set_guild_attr(msg.guild.id, "aliases", guildinfo.aliases, conn)

    await message.send_message(msg, f"Alias: {split_data[2]}\nCommand: {split_data[3]}", title="Alias created")


async def _alias_remove(msg, conn, split_data):
    if len(split_data) < 3:
        await message.invalid_use(msg, help_list.alias, "No alias given")
        return

    split_data[2] = split_data[2].lower()
    guildinfo = guild.load_guild(msg.guild.id, conn)

    if split_data[2] not in guildinfo.aliases.keys():
        await message.send_error(msg, "No alias found")
        return

    guildinfo.aliases.pop(split_data[2])
    guild.set_guild_attr(msg.guild.id, "aliases", guildinfo.aliases, conn)

    await message.send_message(msg, "Alias removed", title="Alias removed")


async def _alias_clear(bot, msg, conn):
    sent_msg = await message.send_message(msg, "Are you sure you want to clear all aliases", title="Clearing..")

    await sent_msg.add_reaction("\u2705")
    await sent_msg.add_reaction("\u274c")

    def reaction_check(reaction, reaction_user):
        if reaction_user != msg.author:
            return False

        if reaction.message != sent_msg:
            return False

        if str(reaction.emoji) != "\u2705" and str(reaction.emoji) != "\u274c":
            return False

        return True

    try:
        reaction, reaction_user = await bot.wait_for("reaction_add", timeout=120, check=reaction_check)
    except asyncio.TimeoutError:
        await message.edit_message(sent_msg, sent_msg.embeds[0].description, title="Timed out")
        return

    if str(reaction.emoji) == "\u274c":
        await message.edit_message(sent_msg, sent_msg.embeds[0].description, title="Cancelled")
        return

    guild.set_guild_attr(msg.guild.id, "aliases", {}, conn)
    await message.edit_message(sent_msg, "All aliases have been cleared", title="Cleared")


async def _alias_list(msg, conn):
    guildinfo = guild.load_guild(msg.guild.id, conn)

    if len(guildinfo.aliases) == 0:
        await message.send_message(msg, "No aliases found", title="Command aliases")
    else:
        await message.send_message(msg, "\n".join([f"{alias}: {guildinfo.aliases[alias]}" for alias in guildinfo.aliases]), title="Command aliases")