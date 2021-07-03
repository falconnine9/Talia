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

#   Command Information   #
name = "kill"
dm_capable = False
# ~~~~~~~~~~~~~~~~~~~~~~~ #

gif_url = "https://raw.githubusercontent.com/Talia-Team/Talia-Assets/main/actiongifs/kill"

self_kill = [
    "Suicide is never the option",
    "Why do you want to kill yourself :(",
    "You can't kill yourself",
    "You're not allowed to kill yourself"
]

suffix = [
    ", rip",
    ", F",
    ""
]


async def run(bot, msg, conn):
    split_data = msg.content.split(" ")

    if len(split_data) < 2:
        await message.invalid_use(msg, help_list.kill, "No user given")
        return

    split_data[1] = split_data[1].replace("<@", "").replace("!", "").replace(">", "")

    try:
        person_id = int(split_data[1])
    except ValueError:
        await message.send_error(msg, "Invalid user")
        return

    if person_id == msg.author.id:
        await message.send_error(msg, random.choice(self_kill))
        return
    else:
        try:
            person = await user.load_user_obj(bot, int(split_data[1]))
        except discord.NotFound:
            await message.send_error(msg, "I can't find that person")
            return
        except discord.HTTPException:
            await message.send_error(msg, "An error occurred and the command couldn't be run")
            return

    random_image = f"{gif_url}/kill{random.randint(1, 7)}.gif"
    await message.send_message(msg, title=f"{str(msg.author)} killed {str(person)}{random.choice(suffix)}",
        img=random_image
    )