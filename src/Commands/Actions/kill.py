"""
Talia Discord Bot
GNU General Public License v3.0
kill.py (Commands/Actions)

kill command
"""
import discord
import random
from Utils import user, message
from Storage import help_list

name = "kill"
dm_capable = False

_gif_url = "https://raw.githubusercontent.com/Talia-Team/Talia-Assets/main/actiongifs/kill"
_self_kill = [
    "Suicide is never the option",
    "Why do you want to kill yourself :(",
    "You can't kill yourself",
    "You're not allowed to kill yourself"
]
_suffix = [
    ", rip",
    ", F",
    ""
]


async def run(args, bot, msg, conn):
    if len(args) < 2:
        await message.invalid_use(msg, help_list.kill, "No user given")
        return

    args[1] = args[1].replace("<@", "").replace("!", "").replace(">", "")

    try:
        person_id = int(args[1])
    except ValueError:
        await message.send_error(msg, "Invalid user")
        return

    if person_id == msg.author.id:
        await message.send_error(msg, random.choice(_self_kill))
        return
    else:
        try:
            person = await user.load_user_obj(bot, int(args[1]))
        except discord.NotFound:
            await message.send_error(msg, "I can't find that person")
            return
        except discord.HTTPException:
            await message.send_error(msg, "An error occurred and the command couldn't be run")
            return

    random_image = f"{_gif_url}/kill{random.randint(1, 7)}.gif"
    await message.send_message(msg, title=f"{str(msg.author)} killed {str(person)}{random.choice(_suffix)}",
        img=random_image
    )