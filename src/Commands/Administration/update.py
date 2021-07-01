"""
Talia Discord Bot
GNU General Public License v3.0
update.py (Commands/Administration)

update command
"""
import discord
import json
from Utils import message, other

#   Command Information   #
name = "update"
dm_capable = False
# ~~~~~~~~~~~~~~~~~~~~~~~ #

required = [
    "version",
    "date"
]


async def run(bot, msg, conn):
    if msg.author.id not in other.load_config().owners:
        await message.send_error(msg, "You have insufficient permissions to use this command")
        return

    split_data = msg.content.split(" ")

    if len(split_data) < 2:
        await message.send_error(msg, "No announcement channel given")
        return

    if len(msg.attachments) == 0:
        await message.send_error(msg, "No update json given")
        return

    filename_split = msg.attachments[0].filename.split(".")

    if filename_split[len(filename_split) - 1] != "json":
        await message.send_error(msg, "The file needs to be a json file")
        return

    data = json.loads((await msg.attachments[0].read()).decode())

    for element in required:
        if element not in data.keys():
            await message.send_error(msg, f"Required element \"{element}\" not found in json file")
            return

    split_data[1] = split_data[1].replace("<#", "").replace(">", "")

    try:
        channel = await other.load_channel_obj(bot, int(split_data[1]))
    except ValueError:
        await message.send_error(msg, "Invalid channel")
        return
    except discord.NotFound:
        await message.send_error(msg, "I can't find that channel")
        return
    except discord.HTTPException:
        await message.send_error(msg, "An error occurred and the command couldn't be run")
        return

    elements = []

    if "added" in data.keys():
        changes = "\n".join([f" **[+]** {change}" for change in data["added"]])
        elements.append(f"**Added**\n{changes}")

    if "removed" in data.keys():
        changes = "\n".join([f" **[-]** {change}" for change in data["removed"]])
        elements.append(f"**Removed**\n{changes}")

    if "fixes" in data.keys():
        changes = "\n".join([f" **[x]** {change}" for change in data["fixes"]])
        elements.append(f"**Fixes**\n{changes}")

    if len(elements) == 0:
        description = "*No changes*"
    else:
        description = "\n\n".join(elements)

    try:
        await message.send_message(None, f"{data['date']}\n\n{description}", channel=channel,
            title=f"Talia version {data['version']}", footer="Updates", footer_icon=bot.user.avatar_url
        )
    except discord.Forbidden:
        await message.send_error(msg, f"I can't send messages in {channel.mention}")