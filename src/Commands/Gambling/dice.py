"""
Talia Discord Bot
GNU General Public License v3.0
dice.py (Commands/Gambling)

dice command
"""
import asyncio
import random
from Utils import user, message, other
from Storage import help_list

name = "dice"
dm_capable = True


async def run(bot, msg, conn):
    split_data = msg.content.split(" ")

    if len(split_data) < 2:
        await message.invalid_use(msg, help_list.dice, "No side given")
        return

    if len(split_data) < 2:
        await message.invalid_use(msg, help_list.dice, "No bet given")
        return

    split_data[1] = split_data[1].lower()

    try:
        side = int(split_data[1])
    except ValueError:
        await message.send_error(msg, f"Unknown side: {split_data[1]}\n(Must be a number between 1-6)")
        return

    if side < 1 or side > 6:
        await message.send_error(msg, f"Unknown side: {split_data[1]}\n(Must be a number between 1-6)")
        return

    split_data[2] = split_data[2].replace(",", "")

    try:
        bet = int(split_data[2])
    except ValueError:
        await message.send_error(msg, "Invalid bet")
        return

    emojis = other.load_emojis(bot)

    if bet < 1:
        await message.send_error(msg, f"You need to bet at least 1 {emojis.coin}")
        return

    userinfo = user.load_user(msg.author.id, conn)

    if bet > userinfo.coins:
        await message.send_error(msg, f"You don't have enough coins to bet {bet:,} {emojis.coin}")
        return

    user.set_user_attr(msg.author.id, "coins", userinfo.coins - bet, conn)
    sent_msg = await message.send_message(msg, f"""Roll cost: -{bet:,} {emojis.coin}
You've bet on side {side}

**Rolling..**""", title="Dice Roll..")
    await asyncio.sleep(random.randint(2, 3))

    userinfo = user.load_user(msg.author.id, conn)
    random_side = random.randint(1, 6)

    if random_side == side:
        user.set_user_attr(msg.author.id, "coins", userinfo.coins + (bet * 6), conn)
        await message.edit_message(sent_msg, f"""Roll cost: -{bet:,} {emojis.coin}
You've bet on side {side}

The dice landed on {random_side}, you earned {(bet * 6):,} {emojis.coin}""", title="You won")

    else:
        await message.edit_message(sent_msg, f"""Roll cost: -{bet:,} {emojis.coin}
You've bet on {side}

The dice landed on {random_side}""", title="You lost")