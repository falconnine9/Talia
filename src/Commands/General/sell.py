"""
Talia Discord Bot
GNU General Public License v3.0
sell.py (Commands/General)

sell command
"""
import asyncio
import discord_components
from Utils import user, subtable, message, other
from Storage import help_list

name = "sell"
dm_capable = True


async def run(args, bot, msg, conn, guildinfo, userinfo):
    if len(args) < 2:
        await message.invalid_use(msg, help_list.sell, "No item given")
        return

    try:
        item = int(args[1]) - 1
    except ValueError:
        await message.send_error(msg, "Invalid item ID")
        return

    if item < 0 or item > len(userinfo.inventory) - 1:
        await message.send_error(msg, "There's no item in your inventory with that ID")
        return

    emojis = other.load_emojis(bot)
    previous_item = userinfo.inventory[item]

    if userinfo.settings.reaction_confirm:
        sent_msg, interaction, result = await _reaction_confirm(bot, msg, userinfo, item, emojis)
    else:
        sent_msg, interaction, result = await _button_confirm(bot, msg, userinfo, item, emojis)

    if result is None:
        return

    if result == "cancel":
        await message.response_edit(sent_msg, interaction, sent_msg.embeds[0].description, title="Cancelled",
            from_reaction=userinfo.settings.reaction_confirm
        )
        return

    userinfo = user.load_user(msg.author.id, conn)

    if item > len(userinfo.inventory) - 1:
        await message.response_send(sent_msg, interaction, "There's no item in your inventory with that ID",
            from_reaction=userinfo.settings.reaction_confirm
        )
        return

    if previous_item != userinfo.inventory[item]:
        await message.response_send(sent_msg, interaction, "The item you've chosen to sell has changed",
            from_reaction=userinfo.settings.reaction_confirm
        )
        return

    user.set_user_attr(msg.author.id, "coins", userinfo.coins + userinfo.inventory[item].worth, conn, False)
    subtable.remove_item(userinfo.inventory[item].id, conn)

    await message.response_edit(sent_msg, interaction,
        f"You sold a {userinfo.inventory[item].name} for {userinfo.inventory[item].worth:,} {emojis.coin}", title="Sold",
        from_reaction=userinfo.settings.reaction_confirm
    )


async def _reaction_confirm(bot, msg, userinfo, item, emojis):
    sent_msg = await message.send_message(msg,
        f"Are you sure you want to sell a {userinfo.inventory[item].name} for {userinfo.inventory[item].worth:,} {emojis.coin}",
        title="Selling.."
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


async def _button_confirm(bot, msg, userinfo, item, emojis):
    sent_msg = await message.send_message(msg,
        f"Are you sure you want to sell a {userinfo.inventory[item].name} for {userinfo.inventory[item].worth:,} {emojis.coin}",
        title="Selling..", components=[[
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
