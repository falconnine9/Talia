"""
Talia Discord Bot
GNU General Public License v3.0
setuserattr.py (Commands/Administration)

setuserattr command
"""
import discord
from Utils import user, message, other


async def run(bot, msg, conn):
    if msg.author.id not in other.load_config().owners:
        await message.send_error(msg, "You have insufficient permissions to use this command")
        return

    split_data = msg.content.split(" ")

    if len(split_data) < 2:
        await message.send_error(msg, "No user given")
        return

    if len(split_data) < 3:
        await message.send_error(msg, "No attribute given")
        return

    if len(split_data) < 4:
        await message.send_error(msg, "No value given")
        return

    split_data[1] = split_data[1].replace("<@", "").replace("!", "").replace(">", "")

    try:
        person = await user.load_user_obj(bot, int(split_data[1]))
    except ValueError:
        await message.send_error(msg, "Invalid user")
        return
    except discord.NotFound:
        await message.send_error(msg, "I can't find that person")
        return
    except discord.HTTPException:
        await message.send_error(msg, "An error occurred and the command couldn't be run")
        return

    if person.bot:
        await message.send_error(msg, "I can't set the attribute of a bot")
        return

    if len(split_data) >= 5:
        if split_data[4] == "int":
            split_data[3] = int(split_data[3])
        elif split_data[4] == "float":
            split_data[3] = float(split_data[3])
        elif split_data[4] == "bool":
            split_data[3] = bool(split_data[3])

    user.set_user_attr(person.id, split_data[2], split_data[3], conn)
    await message.send_message(msg, "Attribute set")