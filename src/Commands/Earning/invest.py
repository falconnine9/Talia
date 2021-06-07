import asyncio

from Utils import user, timer, message, abc, other
from Storage import help_list

times = {
    "8hour": 28800,
    "day": 86400,
    "week": 604800
}

multipliers = {
    "8hour": 1.2,
    "day": 2.5,
    "week": 6
}


async def run(bot, msg, conn):
    invest_timer = timer.load_invest_timer(msg.author.id, conn)

    if invest_timer is not None:
        await message.send_error(msg, f"You've already invested some money, it will be completed in {timer.load_time(invest_timer.time)}")
        return

    split_data = msg.content.split(" ")

    if len(split_data) < 2:
        await message.invalid_use(msg, help_list.invest, "No amount given")
        return

    if len(split_data) < 3:
        await message.invalid_use(msg, help_list.invest, "No time given")
        return

    try:
        amount = int(split_data[1])
    except ValueError:
        await message.send_error(msg, "Invalid amount")
        return

    emojis = other.load_emojis(bot)

    if amount < 1:
        await message.send_error(msg, f"You need to invest at least 1 {emojis.coin}")
        return

    userinfo = user.load_user(msg.author.id, conn)

    if amount > userinfo.coins:
        await message.send_error(msg, f"You don't have enough coins to invest {amount} {emojis.coin}")
        return

    split_data[2] = split_data[2].lower()

    if split_data[2] not in times:
        await message.send_error(msg, f"""Unknown amount of time
`8hour` - Multiply the amount by 1.2x after 8 hours
`day` - Multiply the amount by 2.5x after 1 day
`week` - Multiply the amount by 6x after 1 week""")
        return

    sent_msg = await message.send_message(msg, f"""Are you sure you want to invest {amount} {emojis.coin} for {timer.load_time(times[split_data[2]])}
You will earn {round(amount * multipliers[split_data[2]])} {emojis.coin} and won't be able to invest anything else while you're waiting""", title="Investing..")

    await sent_msg.add_reaction("\u2705")
    await sent_msg.add_reaction("\u274c")

    def reaction_check(reaction, reaction_user):
        if reaction_user != msg.author:
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
        await message.edit_message(sent_msg, sent_msg.embeds[0].description, title="Cancelled")
        return

    userinfo = user.load_user(msg.author.id, conn)

    if amount > userinfo.coins:
        await message.send_error(msg, "You no longer have enough coins for this")
        return

    invest_timer = timer.load_invest_timer(msg.author.id, conn)

    if invest_timer is not None:
        await message.send_error(msg, "You already have an investment going")
        return

    new_timer = abc.InvestTimer(msg.author.id, times[split_data[2]], amount, multipliers[split_data[2]])

    user.set_user_attr(msg.author.id, "coins", userinfo.coins - amount, conn, False)
    timer.new_invest_timer(new_timer, conn)

    await message.edit_message(sent_msg, f"You invested {amount} {emojis.coin} for {timer.load_time(times[split_data[2]])}", title="Invested")