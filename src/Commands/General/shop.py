"""
Talia Discord Bot
GNU General Public License v3.0
shop.py (Commands/General)

shop command
"""
import asyncio
import discord_components
from Utils import guild, user, subtable, message, abc, other
from Storage import help_list

name = "shop"
dm_capable = False


async def run(args, bot, msg, conn, guildinfo, userinfo):
    if len(args) < 2:
        await message.invalid_use(msg, help_list.shop, "No operation given")
        return

    args[1] = args[1].lower()

    if args[1] == "buy":
        await _shop_buy(args, bot, msg, conn, guildinfo, userinfo)
    elif args[1] == "list":
        await _shop_list(bot, msg, guildinfo)
    else:
        await message.send_error(msg, f"Unknown operation: {args[1]}")


async def _shop_buy(args, bot, msg, conn, guildinfo, userinfo):
    if len(args) < 3:
        await message.invalid_use(msg, help_list.shop, "No item given")
        return

    try:
        item = int(args[2]) - 1
    except ValueError:
        await message.send_error(msg, "Invalid item ID")
        return

    if item < 0 or item > len(guildinfo.shop) - 1:
        await message.send_error(msg, "There's no item with that ID in the server shop")
        return

    if len(userinfo.inventory) >= 40:
        await message.send_error(msg, "You don't have any space left in your inventory")
        return

    if guildinfo.shop[item]["cost"] > userinfo.coins:
        await message.send_error(msg, f"You don't have enough coins to buy a {guildinfo.shop[item]['name']}")
        return

    emojis = other.load_emojis(bot)

    if userinfo.settings.reaction_confirm:
        sent_msg, interaction, result = await _reaction_confirm(bot, msg, guildinfo, item, emojis)
    else:
        sent_msg, interaction, result = await _button_confirm(bot, msg, guildinfo, item, emojis)

    if result is None:
        return

    if result == "cancel":
        await message.response_edit(sent_msg, interaction, sent_msg.embeds[0].description, title="Cancelled",
            from_reaction=userinfo.settings.reaction_confirm
        )
        return

    userinfo = user.load_user(msg.author.id, conn)

    if guildinfo.shop[item]["cost"] > userinfo.coins:
        await message.response_send(sent_msg, interaction, "You no longer have enough coins to buy this item",
            from_reaction=userinfo.settings.reaction_confirm
        )
        return

    user.set_user_attr(msg.author.id, "coins", userinfo.coins - guildinfo.shop[item]["cost"], conn, False)
    subtable.new_item(msg.author.id, abc.Item(
        guildinfo.shop[item]["name"], guildinfo.shop[item]["cost"],
        "guild_item", {"from": msg.guild.id}, None
    ), conn)

    await message.response_edit(sent_msg, interaction,
        f"You bought a {guildinfo.shop[item]['name']} for {guildinfo.shop[item]['cost']:,} {emojis.coin}",
        title="Bought", from_reaction=userinfo.settings.reaction_confirm
    )


async def _shop_list(bot, msg, guildinfo):
    if len(guildinfo.shop) == 0:
        await message.send_message(msg, f"{msg.guild.name} has no items in their shop", title="Server shop",
            thumbnail=msg.guild.icon_url
        )
        return

    fields = []
    emojis = other.load_emojis(bot)

    for i, item in enumerate(guildinfo.shop):
        fields.append([item["name"], f"ID: {i + 1}\nCost: {item['cost']:,} {emojis.coin}"])

    await message.send_message(msg, title="Server shop", thumbnail=msg.guild.icon_url, fields=fields)


async def _reaction_confirm(bot, msg, guildinfo, item, emojis):
    sent_msg = await message.send_message(msg,
        f"Are you sure you want to buy a {guildinfo.shop[item]['name']} for {guildinfo.shop[item]['cost']:,} {emojis.coin} from {msg.guild.name}",
        title="Buying.."
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


async def _button_confirm(bot, msg, guildinfo, item, emojis):
    sent_msg = await message.send_message(msg,
        f"Are you sure you want to buy a {guildinfo.shop[item]['name']} for {guildinfo.shop[item]['cost']:,} {emojis.coin} from {msg.guild.name}",
        title="Buying..", components=[[
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