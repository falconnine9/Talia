"""
Talia Discord Bot
GNU General Public License v3.0
divorce.py (Commands/Family)

divorce command
"""
import discord
import random
from Utils import user, message

name = "divorce"
dm_capable = True


async def run(args, bot, msg, conn):
    userinfo = user.load_user(msg.author.id, conn)

    if userinfo.partner is None:
        await message.send_error(msg, "You aren't married")
        return

    try:
        person = await user.load_user_obj(bot, userinfo.partner)
    except discord.NotFound:
        await message.send_error(msg, "An error occurred and the command couldn't be run")
        return
    except discord.HTTPException:
        await message.send_error(msg, "An error occurred and the command couldn't be run")
        return

    children1 = []
    children2 = []

    for child in userinfo.children:
        parent = random.randint(1, 2)
        if parent == 1:
            children1.append(child)
            user.set_user_attr(child, "parents", [msg.author.id], conn, False)
        else:
            children2.append(child)
            user.set_user_attr(child, "parents", [person.id], conn, False)

    user.set_user_attr(msg.author.id, "partner", None, conn, False)
    user.set_user_attr(msg.author.id, "children", children1, conn, False)

    user.set_user_attr(person.id, "partner", None, conn, False)
    user.set_user_attr(person.id, "children", children2, conn)

    await message.send_message(msg, f"You divorced {str(person)}", title="Divorced")

    personinfo = user.load_user(person.id, conn)
    if personinfo.settings.notifs["divorced"]:
        try:
            await message.send_message(None, f"{str(msg.author)} divorced you", title="Divorced", channel=person)
        except discord.Forbidden:
            pass