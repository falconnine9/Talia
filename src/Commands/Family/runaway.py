"""
Talia Discord Bot
GNU General Public License v3.0
runaway.py (Commands/Family)

runaway command
"""
import discord
from Utils import user, message

#   Command Information   #
name = "runaway"
dm_capable = True
# ~~~~~~~~~~~~~~~~~~~~~~~ #


async def run(bot, msg, conn):
    userinfo = user.load_user(msg.author.id, conn)

    if len(userinfo.parents) == 0:
        await message.send_error(msg, f"You don't have any parents to run away from")
        return

    for parent in userinfo.parents:
        parentinfo = user.load_user(parent, conn)
        parentinfo.children.remove(msg.author.id)
        user.set_user_attr(parentinfo.id, "children", parentinfo.children, conn, False)

    user.set_user_attr(msg.author.id, "parents", [], conn)
    await message.send_message(msg, "You ran away from your parents", title="Ran away")

    for parent in userinfo.parents:
        parent_user = await user.load_user_obj(bot, parent)
        parentinfo = user.load_user(parent_user.id, conn)
        if parentinfo.settings.notifs:
            try:
                await message.send_message(None, f"{str(msg.author)} ran away from you", title="Ran away",
                    channel=parent_user
                )
            except discord.Forbidden:
                pass