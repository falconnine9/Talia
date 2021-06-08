import discord

from Utils import user, message
from Storage import help_list


async def run(bot, msg, conn):
    split_data = msg.content.split(" ")

    if len(split_data) < 2:
        await message.invalid_use(msg, help_list.disown, "No user given")
        return

    split_data[1] = split_data[1].replace("<@", "").replace("!", "").replace(">", "")

    try:
        person = await bot.fetch_user(int(split_data[1]))
    except ValueError:
        await message.send_error(msg, "Invalid user")
        return
    except discord.NotFound:
        await message.send_error(msg, "I can't find that person")
        return
    except discord.HTTPException:
        await message.send_error(msg, "An error occurred and the command couldn't be run")
        return

    userinfo = user.load_user(msg.author.id, conn)

    if person.id not in userinfo.children:
        await message.send_error(msg, f"{str(person)} isn't your child")
        return

    userinfo.children.remove(person.id)
    user.set_user_attr(msg.author.id, "children", userinfo.children, conn, False)

    if userinfo.partner is not None:
        partnerinfo = user.load_user(userinfo.partner, conn)
        partnerinfo.children.remove(person.id)
        user.set_user_attr(partnerinfo.id, "children", partnerinfo.children, conn, False)

    user.set_user_attr(person.id, "parents", [], conn)
    await message.send_message(msg, f"{str(person)} is not longer your child", title="Disowned")

    try:
        await message.send_message(None, f"{str(msg.author)} disowned you", title="Disowned", channel=person)
    except discord.Forbidden:
        pass