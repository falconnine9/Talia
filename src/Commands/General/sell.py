"""
Talia Discord Bot
GNU General Public License v3.0
sell.py (Commands/General)

sell command
"""
import asyncio
import discord_components
from Utils import user, message, other
from Storage import help_list

#   Command Information   #
name = "sell"
dm_capable = True
# ~~~~~~~~~~~~~~~~~~~~~~~ #


async def run(bot, msg, conn):
    split_data = msg.content.split(" ")

    if len(split_data) < 2:
        await message.invalid_use(msg, help_list.sell, "No item given")
        return

    try:
        item = int(split_data[1]) - 1
    except ValueError:
        await message.send_error(msg, "Invalid item ID")
        return

    userinfo = user.load_user(msg.author.id, conn)

    if item < 0 or item > len(userinfo.inventory) - 1:
        await message.send_error(msg, "There's no item in your inventory with that ID")
        return

    emojis = other.load_emojis(bot)
    sent_msg = await message.send_message(msg,
        f"Are you sure you want to sell a {userinfo.inventory[item].name} for {userinfo.inventory[item].worth} {emojis.coin}",
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
        return

    if interaction.component.label == "Cancel":
        await message.response_edit(sent_msg, interaction, sent_msg.embeds[0].description, title="Cancelled")
        return

    userinfo = user.load_user(msg.author.id, conn)

    if item > len(userinfo.inventory) - 1:
        await message.response_send(sent_msg, interaction, "There's no item in your inventory with that ID")
        return

    await message.response_edit(sent_msg, interaction, f"You sold a {userinfo.inventory[item].name} for {userinfo.inventory[item].worth} {emojis.coin}", title="Sold")

    user.set_user_attr(msg.author.id, "coins", userinfo.inventory[item].worth, conn, False)
    userinfo.inventory.pop(item)
    user.set_user_attr(msg.author.id, "inventory", userinfo.inventory, conn)