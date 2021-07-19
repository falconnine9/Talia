"""
Talia Discord Bot
GNU General Public License v3.0
coinflip.py (Commands/Gambling)

coinflip command
"""
import asyncio
import random
from Utils import user, message, other
from Storage import help_list

name = "coinflip"
dm_capable = True

_sides = ["heads", "tails"]


async def run(args, bot, msg, conn, guildinfo, userinfo):
    if len(args) < 2:
        await message.invalid_use(msg, help_list.coinflip, "No side given")
        return

    if len(args) < 3:
        await message.invalid_use(msg, help_list.coinflip, "No bet given")
        return

    args[1] = args[1].lower()

    if args[1] not in _sides:
        await message.send_error(msg, f"Unknown side: {args[1]}\n(`heads` or `tails`)")
        return

    args[2] = args[2].replace(",", "")

    try:
        bet = int(args[2])
    except ValueError:
        await message.send_error(msg, "Invalid bet")
        return

    emojis = other.load_emojis(bot)

    if bet < 1:
        await message.send_error(msg, f"You need to bet at least 1 {emojis.coin}")

    if bet > userinfo.coins:
        await message.send_error(msg, f"You don't have enough coins to bet {bet:,} {emojis.coin}")
        return

    user.set_user_attr(msg.author.id, "coins", userinfo.coins - bet, conn)
    sent_msg = await message.send_message(msg, f"""Flip cost: -{bet:,} {emojis.coin}
You've bet on {args[1]}

**Flipping..**""", title="Coinflip..")
    await asyncio.sleep(random.randint(2, 3))

    userinfo = user.load_user(msg.author.id, conn)
    random_side = random.choice(_sides)

    if random_side == args[1]:
        user.set_user_attr(msg.author.id, "coins", userinfo.coins + (bet * 2), conn)
        await message.edit_message(sent_msg, f"""Flip cost: -{bet:,} {emojis.coin}
You've bet on {args[1]}

The coin landed on {random_side}, you earned {(bet * 2):,} {emojis.coin}""", title="You won")

    else:
        await message.edit_message(sent_msg, f"""Flip cost: -{bet:,} {emojis.coin}
You've bet on {args[1]}

The coin landed on {random_side}""", title="You lost")