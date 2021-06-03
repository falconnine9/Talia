import asyncio
import random

from Utils import user, message, other
from Storage import help_list

sides = ["heads", "tails"]


async def run(bot, msg, conn):
    split_data = msg.content.split(" ")

    if len(split_data) < 2:
        await message.invalid_use(msg, help_list.coinflip, "No side given")
        return

    if len(split_data) < 3:
        await message.invalid_use(msg, help_list.coinflip, "No bet given")
        return

    split_data[1] = split_data[1].lower()

    if split_data[1] not in sides:
        await message.send_error(msg, f"Unknown side: {split_data[1]}\n(`heads` or `tails`)")
        return

    try:
        bet = int(split_data[2])
    except ValueError:
        await message.send_error(msg, "Invalid bet")
        return

    emojis = other.load_emojis(bot)

    if bet < 1:
        await message.send_error(msg, f"You need to bet at least 1 {emojis.coin}")

    userinfo = user.load_user(msg.author.id, conn)

    if bet > userinfo.coins:
        await message.send_error(msg, f"You don't have enough coins to bet {bet} {emojis.coin}")
        return

    user.set_user_attr(msg.author.id, "coins", userinfo.coins - bet, conn)
    sent_msg = await message.send_message(msg, f"""Flip cost: -{bet} {emojis.coin}
You've bet on {split_data[1]}

**Flipping..**""", title="Coinflip..")
    await asyncio.sleep(random.randint(2, 3))

    userinfo = user.load_user(msg.author.id, conn)
    random_side = random.choice(sides)

    if random_side == split_data[1]:
        user.set_user_attr(msg.author.id, "coins", userinfo.coins + (bet * 2), conn)
        await message.edit_message(sent_msg, f"""Flip cost: -{bet} {emojis.coin}
You've bet on {split_data[1]}

The coin landed on {random_side}, you earned {bet * 2} {emojis.coin}""", title="You won")

    else:
        await message.edit_message(sent_msg, f"""Flip cost: -{bet} {emojis.coin}
You've bet on {split_data[1]}

The coin landed on {random_side}""", title="You lost")