import asyncio
import discord
import random

from Utils import user, message, other
from Storage import help_list

already_married = [
    "But you're already married",
    "You're already married"
]

parent_marry = [
    "{user} is your parent",
    "You can't marry your parent..",
    "Why do you want to marry {user}? They're your parent"
]

children_marry = [
    "{user} is your child",
    "You can't marry your child!"
]


async def run(bot, msg, conn):
    userinfo = user.load_user(msg.author.id, conn)

    if userinfo.partner is not None:
        await message.send_error(msg, random.choice(already_married))
        return

    split_data = msg.content.split(" ")

    if len(split_data) < 2:
        await message.invalid_use(msg, help_list.marry, "No user given")
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

    if person.bot:
        await message.send_error(msg, "You can't marry a bot")
        return

    if person.id in userinfo.parents:
        await message.send_error(msg, random.choice(parent_marry).replace("{user}", str(person)))
        return

    if person.id in userinfo.children:
        await message.send_error(msg, random.choice(children_marry).replace("{user}", str(person)))
        return

    personinfo = user.load_user(msg.author.id, conn)

    if personinfo.partner is not None:
        await message.send_error(msg, f"{str(person)} is already married")
        return

    sent_msg = await message.send_message(msg, f"{str(msg.author)} has proposed to {str(person)}", title="Proposal..")

    await sent_msg.add_reaction("\u2705")
    await sent_msg.add_reaction("\u274c")

    def reaction_check(reaction, reaction_user):
        if reaction_user != person:
            return False

        if reaction.message != sent_msg:
            return False

        if str(reaction.emoji) != "\u2705" and str(reaction.emoji) != "\u274c":
            return False

        return True

    try:
        reaction, reaction_user = await bot.wait_for("reaction_add", timeout=120, check=reaction_check)
    except asyncio.TimeoutError:
        await message.edit_message(sent_msg, sent_msg.embeds[0].description, title="Timed out")
        return

    if str(reaction.emoji) == "\u274c":
        await message.edit_message(sent_msg, sent_msg.embeds[0].description, title="Declined")
        return

    userinfo = user.load_user(msg.author.id, conn)
    personinfo = user.load_user(msg.author.id, conn)

    if userinfo.partner is not None:
        await message.send_error(msg, f"{str(msg.author)} is already married")
        return

    if personinfo.partner is not None:
        await message.send_error(msg, "You're already married")
        return

    if msg.author.id in personinfo.parents:
        await message.send_error(msg, f"{str(msg.author)} is your parent")
        return

    if msg.author.id in personinfo.children:
        await message.send_error(msg, f"{str(msg.author)} is your child")
        return

    new_children = []

    for child in userinfo.children:
        user.set_user_attr(msg.author.id, "parents", [msg.author.id, person.id], conn, False)
        new_children.append(child)

    for child in personinfo.children:
        user.set_user_attr(msg.author.id, "parents", [person.id, msg.author.id], conn, False)
        new_children.append(child)

    user.set_user_attr(msg.author.id, "partner", person.id, conn, False)
    user.set_user_attr(msg.author.id, "children", new_children, conn, False)

    user.set_user_attr(person.id, "partner", msg.author.id, conn, False)
    user.set_user_attr(person.id, "children", new_children, conn)

    emojis = other.load_emojis(bot)
    await message.edit_message(sent_msg, f"{emojis.confetti} {str(msg.author)} married {str(person)} {emojis.confetti}", title="Married")