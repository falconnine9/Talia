"""
Talia Discord Bot
GNU General Public License v3.0
balance.py (Commands/General)

balance command
"""
import random
from Utils import user, message, other

name = "balance"
dm_capable = True

_no_coins = [
    "You have no coins :(",
    "You don't have any coins",
    "No coins lol poor"
]


async def run(args, bot, msg, conn, guildinfo, userinfo):
    emojis = other.load_emojis(bot)

    if userinfo.coins == 0:
        await message.send_message(msg, random.choice(_no_coins), title="Your balance")
        return
    else:
        await message.send_message(msg, f"You have {userinfo.coins:,} {emojis.coin}", title="Your balance")