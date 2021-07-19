"""
Talia Discord Bot
GNU General Public License v3.0
pat.py (Commands/Actions)

pat command
"""
import discord
import random
from Utils import user, message
from Storage import help_list

name = "pat"
dm_capable = False

_gif_url = "https://raw.githubusercontent.com/Talia-Team/Talia-Assets/main/actiongifs/pat"
_self_pat = [
    "You can't pat yourself",
    "You should get someone else to pat you"
]
_suffix = [
    " :)",
    ", aww",
    ", cute"
]


async def run(args, bot, msg, conn, guildinfo, userinfo):
    if len(args) < 2:
        await message.invalid_use(msg, help_list.pat, "No user given")
        return

    args[1] = args[1].replace("<@", "").replace("!", "").replace(">", "")

    try:
        person_id = int(args[1])
    except ValueError:
        await message.send_error(msg, "Invalid user")
        return

    if person_id == msg.author.id:
        await message.send_error(msg, random.choice(_self_pat))
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

    random_image = f"{_gif_url}/pat{random.randint(1, 18)}.gif"
    await message.send_message(msg, title=f"{str(msg.author)} patted {str(person)}{random.choice(_suffix)}",
        img=random_image
    )