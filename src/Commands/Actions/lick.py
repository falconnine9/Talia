"""
Talia Discord Bot
GNU General Public License v3.0
lick.py (Commands/Actions)

lick command
"""
import discord
import random
from Utils import user, message
from Storage import help_list

#   Command Information   #
name = "lick"
dm_capable = False
# ~~~~~~~~~~~~~~~~~~~~~~~ #

gif_url = "https://raw.githubusercontent.com/Talia-Team/Talia-Assets/main/actiongifs/lick"

self_lick = [
    "You wanna lick yourself? Kinda weird",
    "You can't lick yourself",
]

suffix = [
    ", kinky",
    ", uwu",
]


async def run(bot, msg, conn):
    split_data = msg.content.split(" ")

    if len(split_data) < 2:
        await message.invalid_use(msg, help_list.lick, "No user given")
        return

    split_data[1] = split_data[1].replace("<@", "").replace("!", "").replace(">", "")

    try:
        person_id = int(split_data[1])
    except ValueError:
        await message.send_error(msg, "Invalid user")
        return

    if person_id == msg.author.id:
        await message.send_error(msg, random.choice(self_lick))
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

    random_image = f"{gif_url}/lick{random.randint(1, 20)}.gif"
    await message.send_message(msg, title=f"{str(msg.author)} licked {str(person)}{random.choice(suffix)}",
        img=random_image
    )