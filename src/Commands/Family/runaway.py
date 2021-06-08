import discord

from Utils import user, message


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
        parent_user = await bot.fetch_user(parent)
        try:
            await message.send_message(None, f"{str(msg.author)} ran away from you", title="Ran away", channel=parent_user)
        except discord.Forbidden:
            pass