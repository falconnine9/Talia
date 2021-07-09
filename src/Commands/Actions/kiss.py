"""
Talia Discord Bot
GNU General Public License v3.0
kiss.py (Commands/Actions)

kiss command
"""
import discord
import random
from Utils import user, message
from Storage import help_list

name = "kiss"
dm_capable = False

_gif_url = "https://raw.githubusercontent.com/Talia-Team/Talia-Assets/main/actiongifs/kiss"
_self_kiss = [
    "You can't kiss yourself",
    "How are you gonna kiss yourself",
    "You can't kiss yourself :("
]
_suffix = [
    " :)",
    ", aww",
    ", cute"
]


async def run(bot, msg, conn):
    split_data = msg.content.split(" ")

    if len(split_data) < 2:
        await message.invalid_use(msg, help_list.kiss, "No user given")
        return

    split_data[1] = split_data[1].replace("<@", "").replace("!", "").replace(">", "")

    try:
        person_id = int(split_data[1])
    except ValueError:
        await message.send_error(msg, "Invalid user")
        return

    if person_id == msg.author.id:
        await message.send_error(msg, random.choice(_self_kiss))
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

    random_image = f"{_gif_url}/kiss{random.randint(1, 18)}.gif"
    await message.send_message(msg, title=f"{str(msg.author)} kissed {str(person)}{random.choice(_suffix)}",
        img=random_image
    )