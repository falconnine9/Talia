"""
Talia Discord Bot
GNU General Public License v3.0
setuserattr.py (Commands/Administration)

setuserattr command
"""
import discord
from Utils import user, message, other

name = "setuserattr"
dm_capable = True


async def run(args, bot, msg, conn):
    if msg.author.id not in other.load_config().owners:
        await message.send_error(msg, "You have insufficient permissions to use this command")
        return

    if len(args) < 2:
        await message.send_error(msg, "No user given")
        return

    if len(args) < 3:
        await message.send_error(msg, "No attribute given")
        return

    if len(args) < 4:
        await message.send_error(msg, "No value given")
        return

    args[1] = args[1].replace("<@", "").replace("!", "").replace(">", "")

    try:
        person = await user.load_user_obj(bot, int(args[1]))
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

    if len(args) >= 5:
        if args[4] == "int":
            args[3] = int(args[3])
        elif args[4] == "float":
            args[3] = float(args[3])
        elif args[4] == "bool":
            args[3] = bool(args[3])

    user.set_user_attr(person.id, args[2], args[3], conn)
    await message.send_message(msg, "Attribute set")