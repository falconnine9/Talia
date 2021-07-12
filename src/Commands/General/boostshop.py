"""
Talia Discord Bot
GNU General Public License v3.0
boostshop.py (Commands/General)

boostshop command
"""
import asyncio
import discord_components
from Utils import user, message, other
from Storage import help_list

name = "boostshop"
dm_capable = True

_boosts = {
    "multiplier": {
        "name": "Multiplier",
        "desc": "Add +0.1 onto your multiplier"
    }
}


async def run(bot, msg, conn):
    split_data = msg.content.split(" ")

    if len(split_data) < 2:
        await message.invalid_use(msg, help_list.boostshop, "No operation given")
        return

    split_data[1] = split_data[1].lower()

    if split_data[1] == "buy":
        await _boostshop_buy(bot, msg, conn, split_data)

    elif split_data[1] == "list":
        await _boostshop_list(bot, msg, conn)

    else:
        await message.send_error(msg, f"Unknown operation: {split_data[1]}")


async def _boostshop_buy(bot, msg, conn, split_data):
    if len(split_data) < 3:
        await message.invalid_use(msg, help_list.boostshop, "No boost given")
        return

    split_data[2] = split_data[2].lower()

    if split_data[2] not in _boosts.keys():
        await message.send_error(msg, f"There's no boost in the shop named \"{split_data[2]}\"")
        return

    userinfo = user.load_user(msg.author.id, conn)

    if split_data[2] == "multiplier":
        cost = userinfo.shop_info.multiplier_cost
    else:
        cost = 0

    if cost > userinfo.coins:
        await message.send_error(msg, f"You don't have enough coins to buy a {_boosts[split_data[2]]['name']} boost")
        return

    emojis = other.load_emojis(bot)

    if userinfo.settings.reaction_confirm:
        sent_msg, interaction, result = await _reaction_confirm(bot, msg, split_data[2], cost, emojis)
    else:
        sent_msg, interaction, result = await _button_confirm(bot, msg, split_data[2], cost, emojis)

    if result is None:
        return

    if result == "cancel":
        await message.response_edit(sent_msg, interaction, sent_msg.embeds[0].description, title="Cancelled",
            from_reaction=userinfo.settings.reaction_confirm
        )
        return

    userinfo = user.load_user(msg.author.id, conn)

    if split_data[2] == "multiplier":
        cost = userinfo.shop_info.multiplier_cost
    else:
        cost = 0

    if cost > userinfo.coins:
        await message.response_send(sent_msg, interaction, "You no longer have enough coins to buy this boost",
            from_reaction=userinfo.settings.reaction_confirm
        )
        return

    if split_data[2] == "multiplier":
        userinfo.shop_info.multiplier_cost *= 2
        user.set_user_attr(msg.author.id, "multiplier", round(userinfo.multiplier + 0.1, 1), conn, False)

    user.set_user_attr(msg.author.id, "coins", userinfo.coins - cost, conn, False)
    user.set_user_attr(msg.author.id, "shop_info", userinfo.shop_info.cvt_dict(), conn)

    await message.response_edit(sent_msg, interaction,
        f"You bought a {_boosts[split_data[2]]['name']} boost for {cost:,} {emojis.coin}", title="Bought",
        from_reaction=userinfo.settings.reaction_confirm
    )


async def _boostshop_list(bot, msg, conn):
    userinfo = user.load_user(msg.author.id, conn)
    fields = []
    emojis = other.load_emojis(bot)

    for boost in _boosts:
        if boost == "multiplier":
            cost = userinfo.shop_info.multiplier_cost
        else:
            cost = 0
        fields.append([_boosts[boost]["name"], f"{_boosts[boost]['desc']}\nCost: {cost:,} {emojis.coin}"])

    await message.send_message(msg, title="Boost shop", footer="Costs may only be applicable to you", fields=fields)


async def _reaction_confirm(bot, msg, boost, cost, emojis):
    sent_msg = await message.send_message(msg,
        f"Are you sure you want to buy a {_boosts[boost]['name']} boost for {cost:,} {emojis.coin}", title="Buying.."
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


async def _button_confirm(bot, msg, boost, cost, emojis):
    sent_msg = await message.send_message(msg,
        f"Are you sure you want to buy a {_boosts[boost]['name']} boost for {cost:,} {emojis.coin}", title="Buying..",
        components=[[
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