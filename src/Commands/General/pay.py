"""
Talia Discord Bot
GNU General Public License v3.0
pay.py (Commands/General)

pay command
"""
import discord
import random
from Utils import user, message, other
from Storage import help_list

#   Command Information   #
name = "pay"
dm_capable = True
# ~~~~~~~~~~~~~~~~~~~~~~~ #

self_pay = [
    "You can't pay yourself",
    "Um, you can't pay yourself",
    "Sorry, you can't pay yourself"
]


async def run(bot, msg, conn):
    split_data = msg.content.split(" ")

    if len(split_data) < 2:
        await message.invalid_use(msg, help_list.pay, "No user given")
        return

    if len(split_data) < 3:
        await message.invalid_use(msg, help_list.pay, "No amount given")
        return

    split_data[1] = split_data[1].replace("<@", "").replace("!", "").replace(">", "")

    try:
        person_id = int(split_data[1])
    except ValueError:
        await message.send_error(msg, "Invalid user")
        return

    if person_id == msg.author.id:
        await message.send_error(msg, random.choice(self_pay))
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

    if person.bot:
        await message.send_error(msg, "You can't pay a bot")
        return

    try:
        amount = int(split_data[2])
    except ValueError:
        await message.send_error(msg, "Invalid amount")
        return

    emojis = other.load_emojis(bot)

    if amount < 1:
        await message.send_error(msg, f"You have to pay at least 1 {emojis.coin}")
        return

    userinfo = user.load_user(msg.author.id, conn)

    if amount > userinfo.coins:
        await message.send_error(msg, f"You don't have {amount:,} {emojis.coin}")
        return

    personinfo = user.load_user(person.id, conn)

    user.set_user_attr(msg.author.id, "coins", userinfo.coins - amount, conn, False)
    user.set_user_attr(person.id, "coins", personinfo.coins + amount, conn)

    await message.send_message(msg, f"You paid {str(person)} {amount:,} {emojis.coin}", title="Paid")

    if personinfo.settings.notifs["paid"]:
        try:
            await message.send_message(None, f"{str(msg.author)} paid you {amount:,} {emojis.coin}", channel=person)
        except discord.Forbidden:
            pass