"""
Talia Discord Bot
GNU General Public License v3.0
invest.py (Commands/Earning)

invest command
"""
import asyncio
import discord_components
import random
from Utils import user, timer, message, abc, other
from Storage import help_list

name = "invest"
dm_capable = True

_times = {
    "short": [8, 24],
    "long": [24, 96]
}  # Random number in between the 2 in the list
_multipliers = {
    "short": [1.8, 2.7],
    "long": [1.3, 1.9]
}  # Random number in between the 2 in the list
_failed_chances = {
    "short": [0.6, 0.75],
    "long": [0.15, 0.4]
}  # Random number in between the 2 in the list
_loss_amounts = {
    "short": [0.5, 0.75],
    "long": [0.25, 0.5]
}  # Random number in between the 2 in the list


async def run(bot, msg, conn):
    invest_timer = timer.load_invest_timer(msg.author.id, conn)

    if invest_timer is not None:
        await message.send_error(msg,
            f"You've already invested some coins, it will be completed in {timer.load_time(invest_timer.time)}"
        )
        return

    split_data = msg.content.split(" ")

    if len(split_data) < 2:
        await message.invalid_use(msg, help_list.invest, "No amount given")
        return

    if len(split_data) < 3:
        await message.invalid_use(msg, help_list.invest, "No time given")
        return

    split_data[1] = split_data[1].replace(",", "")

    try:
        amount = int(split_data[1])
    except ValueError:
        await message.send_error(msg, "Invalid amount")
        return

    emojis = other.load_emojis(bot)

    if amount < 100:
        await message.send_error(msg, f"You need to invest at least 100 {emojis.coin}")
        return

    userinfo = user.load_user(msg.author.id, conn)

    if amount > userinfo.coins:
        await message.send_error(msg, f"You don't have enough coins to invest {amount:,} {emojis.coin}")
        return

    split_data[2] = split_data[2].lower()

    if split_data[2] not in _times:
        await message.send_error(msg, f"""Invalid time
`short` - Short term, high reward but high risk
`long` - Long term, small reward and small risk""")
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

    random_time = random.randint(_times[split_data[2]][0], _times[split_data[2]][1]) * 60 * 60
    random_multi = round(random.uniform(_multipliers[split_data[2]][0], _multipliers[split_data[2]][1]), 1)
    failed = random.random() < round(
        random.uniform(_failed_chances[split_data[2]][0], _failed_chances[split_data[2]][1]), 1
    )

    if failed:
        loss = round(random.uniform(_loss_amounts[split_data[2]][0], _loss_amounts[split_data[2]][1]), 2)
    else:
        loss = None

    new_timer = abc.InvestTimer(msg.author.id, random_time, amount, random_multi, failed, loss)

    user.set_user_attr(msg.author.id, "coins", userinfo.coins - amount, conn, False)
    timer.new_invest_timer(new_timer, conn)

    await message.response_edit(sent_msg, interaction,
        f"You invested {amount:,} {emojis.coin} for {timer.load_time(random_time)}", title="Invested",
        from_reaction=userinfo.settings.reaction_confirm
    )


async def _reaction_confirm(bot, msg, split_data, amount, emojis):
    sent_msg = await message.send_message(msg, f"""Are you sure you want to invest {amount:,} {emojis.coin}

It will take in between {_times[split_data[2]][0]}h to {_times[split_data[2]][1]}h to complete
And you will earn in between {round(_multipliers[split_data[2]][0] * amount):,} {emojis.coin} to {round(_multipliers[split_data[2]][1] * amount):,} {emojis.coin}""",
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
    sent_msg = await message.send_message(msg, f"""Are you sure you want to invest {amount:,} {emojis.coin}

It will take in between {_times[split_data[2]][0]}h to {_times[split_data[2]][1]}h to complete
And you will earn in between {(round(_multipliers[split_data[2]][0] * amount)):,} {emojis.coin} to {(round(_multipliers[split_data[2]][1] * amount)):,} {emojis.coin}""",
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