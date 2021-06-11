"""
Talia Discord Bot
GNU General Public License v3.0
bal.py (Commands/General)

bal command
"""
import random
from Utils import user, message, other

no_coins = [
    "You have no coins :(",
    "You don't have any coins",
    "No coins lol poor"
]


async def run(bot, msg, conn):
    userinfo = user.load_user(msg.author.id, conn)
    emojis = other.load_emojis(bot)

    if userinfo.coins == 0:
        await message.send_message(msg, random.choice(no_coins), title="Your balance")
        return
    else:
        await message.send_message(msg, f"You have {userinfo.coins} {emojis.coin}", title="Your balance")