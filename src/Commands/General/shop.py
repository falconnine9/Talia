"""
Talia Discord Bot
GNU General Public License v3.0
shop.py (Commands/General)

shop command
"""
import asyncio
import discord_components
from Utils import guild, user, message, abc, other
from Storage import help_list


async def run(bot, msg, conn):
    split_data = msg.content.split(" ")

    if len(split_data) < 2:
        await message.invalid_use(msg, help_list.shop, "No operation given")
        return

    split_data[1] = split_data[1].lower()

    if split_data[1] == "buy":
        await _shop_buy(bot, msg, conn, split_data)

    elif split_data[1] == "list":
        await _shop_list(bot, msg, conn)

    else:
        await message.send_error(msg, f"Unknown operation: {split_data[1]}")


async def _shop_buy(bot, msg, conn, split_data):
    if len(split_data) < 3:
        await message.invalid_use(msg, help_list.shop, "No item given")
        return

    try:
        item = int(split_data[2]) - 1
    except ValueError:
        await message.send_error(msg, "Invalid item ID")
        return

    guildinfo = guild.load_guild(msg.guild.id, conn)

    if item < 0 or item > len(guildinfo.shop) - 1:
        await message.send_error(msg, "There's no item with that ID in the server shop")
        return

    userinfo = user.load_user(msg.author.id, conn)

    if len(userinfo.inventory) >= 40:
        await message.send_error(msg, "You don't have any space left in your inventory")
        return

    if guildinfo.shop[item]["cost"] > userinfo.coins:
        await message.send_error(msg, f"You don't have enough coins to buy a {guildinfo.shop[item]['name']}")
        return

    emojis = other.load_emojis(bot)
    sent_msg = await message.send_message(msg, f"Are you sure you want to buy a {guildinfo.shop[item]['name']} for {guildinfo.shop[item]['cost']} {emojis.coin} from {msg.guild.name}", title="Buying..",
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
        await message.edit_message(sent_msg, sent_msg.embeds[0].description, title="Timed out", components=[])
        return

    if interaction.component.label == "Cancel":
        await message.edit_message(sent_msg, sent_msg.embeds[0].description, title="Cancelled", components=[])
        return

    userinfo = user.load_user(msg.author.id, conn)

    if guildinfo.shop[item]["cost"] > userinfo.coins:
        await message.edit_message(sent_msg, sent_msg.embeds[0].description, title="Buying..", components=[])
        await message.send_error(msg, "You no longer have enough coins to buy this item")
        return

    userinfo.inventory.append(abc.Item(
        guildinfo.shop[item]["name"],
        guildinfo.shop[item]["cost"],
        "guild_item", {"from": msg.guild.id}
    ))

    user.set_user_attr(msg.author.id, "coins", userinfo.coins - guildinfo.shop[item]["cost"], conn, False)
    user.set_user_attr(msg.author.id, "inventory", userinfo.inventory, conn)

    await message.edit_message(sent_msg, f"You bought a {guildinfo.shop[item]['name']} for {guildinfo.shop[item]['cost']} {emojis.coin}", title="Bought", components=[])


async def _shop_list(bot, msg, conn):
    guildinfo = guild.load_guild(msg.guild.id, conn)

    if len(guildinfo.shop) == 0:
        await message.send_message(msg, f"{msg.guild.name} has no items in their shop", title="Server shop", thumbnail=msg.guild.icon_url)
        return

    fields = []
    emojis = other.load_emojis(bot)

    for i, item in enumerate(guildinfo.shop):
        fields.append([item["name"], f"ID: {i + 1}\nCost: {item['cost']} {emojis.coin}"])

    await message.send_message(msg, title="Server shop", thumbnail=msg.guild.icon_url, fields=fields)