"""
Talia Discord Bot
GNU General Public License v3.0
invest.py (Commands/Earning)

invest command
"""
import asyncio
import discord_components
from Utils import user, timer, message, abc, other
from Storage import help_list

#   Command Information   #
name = "invest"
dm_capable = True
# ~~~~~~~~~~~~~~~~~~~~~~~ #

times = {
    "8hour": 28800,
    "day": 86400,
    "3day": 259200,
    "week": 604800
}

multipliers = {
    "8hour": 1.2,
    "day": 1.7,
    "3day": 5,
    "week": 11
}


async def run(bot, msg, conn):
    invest_timer = timer.load_invest_timer(msg.author.id, conn)

    if invest_timer is not None:
        emojis = other.load_emojis(bot)
        await message.send_error(msg,
            f"""You've already invested some money

Time remaining: {timer.load_time(invest_timer.time)}
Invested: {invest_timer.coins} {emojis.coin}
Returning: {round(invest_timer.coins * invest_timer.multiplier)} {emojis.coin}"""
        )
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
`8hour` - Multiply the amount by x1.2 after 8 hours
`day` - Multiply the amount by x1.7 after 1 day
`3day` - Multiply the amount by x5 after 3 days
`week` - Multiply the amount by x11 after 1 week""")
        return

    if userinfo.settings.reaction_confirm:
        sent_msg, interaction, result = await _reaction_confirm(bot, msg, split_data, amount, emojis)
    else:
        sent_msg, interaction, result = await _button_confirm(bot, msg, split_data, amount, emojis)

    if result is None:
        return

    if result == "cancel":
        await message.response_edit(sent_msg, interaction, sent_msg.embeds[0].description, title="Cancelled",
            from_reaction=userinfo.settings.reaction_confirm
        )
        return

    userinfo = user.load_user(msg.author.id, conn)

    if amount > userinfo.coins:
        await message.response_send(sent_msg, interaction, "You no longer have enough coins for this",
            from_reaction=userinfo.settings.reaction_confirm
        )
        return

    invest_timer = timer.load_invest_timer(msg.author.id, conn)

    if invest_timer is not None:
        await message.response_send(sent_msg, interaction, "You already have an investment going",
            from_reaction=userinfo.settings.reaction_confirm
        )
        return

    new_timer = abc.InvestTimer(msg.author.id, times[split_data[2]], amount, multipliers[split_data[2]])

    user.set_user_attr(msg.author.id, "coins", userinfo.coins - amount, conn, False)
    timer.new_invest_timer(new_timer, conn)

    await message.response_edit(sent_msg, interaction,
        f"You invested {amount} {emojis.coin} for {timer.load_time(times[split_data[2]])}", title="Invested",
        from_reaction=userinfo.settings.reaction_confirm
    )


async def _reaction_confirm(bot, msg, split_data, amount, emojis):
    sent_msg = await message.send_message(msg,
        f"""Are you sure you want to invest {amount} {emojis.coin} for {timer.load_time(times[split_data[2]])}
You will earn {round(amount * multipliers[split_data[2]])} {emojis.coin} and won't be able to invest anything else while you're waiting""",
        title="Investing.."
    )

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
        await message.timeout_response(sent_msg, from_reaction=True)
        return None, None, None

    if str(reaction.emoji) == "\u2705":
        return sent_msg, None, "confirm"
    else:
        return sent_msg, None, "cancel"


async def _button_confirm(bot, msg, split_data, amount, emojis):
    sent_msg = await message.send_message(msg,
        f"""Are you sure you want to invest {amount} {emojis.coin} for {timer.load_time(times[split_data[2]])}
You will earn {round(amount * multipliers[split_data[2]])} {emojis.coin} and won't be able to invest anything else while you're waiting""",
        title="Investing..", components=[[
            discord_components.Button(label="Confirm", style=discord_components.ButtonStyle.green),
            discord_components.Button(label="Cancel", style=discord_components.ButtonStyle.red)
        ]]
    )

    def button_check(interaction):
        if interaction.author != msg.author:
            return False

        if interaction.message != sent_msg:
            return False

        return True

    try:
        interaction = await bot.wait_for("button_click", timeout=120, check=button_check)
    except asyncio.TimeoutError:
        await message.timeout_response(sent_msg)
        return None, None, None

    if interaction.component.label == "Confirm":
        return sent_msg, interaction, "confirm"
    else:
        return sent_msg, interaction, "cancel"