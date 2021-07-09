"""
Talia Discord Bot
GNU General Public License v3.0
inventory.py (Commands/General)

inventory command
"""
import discord
from Utils import user, message

name = "inventory"
dm_capable = True


async def run(bot, msg, conn):
    split_data = msg.content.split(" ")

    if len(split_data) < 2:
        split_data.append(str(msg.author.id))
    else:
        split_data[1] = split_data[1].replace("<@", "").replace("!", "").replace(">", "")

    try:
        person_id = int(split_data[1])
    except ValueError:
        await message.send_error(msg, "Invalid user")
        return

    if person_id == msg.author.id:
        person = msg.author
    else:
        try:
            person = await user.load_user_obj(bot, int(split_data[1]))
        except discord.NotFound:
            await message.send_error(msg, "I can't find that person")
            return
        except discord.HTTPException:
            await message.send_error(msg, "An error occurred and the command couldn't be run")
            return

    if person.bot:
        await message.send_error(msg, "I can't get the inventory of a bot")
        return

    personinfo = user.load_user(person.id, conn)
    await message.send_message(msg,
        "\n".join([f"ID {i + 1}: {item.name}" for i, item in enumerate(personinfo.inventory)]),
        title=f"{str(person)}'s inventory", thumbnail=person.avatar_url,
        footer=f"{len(personinfo.inventory)}/40 items", color=personinfo.color)