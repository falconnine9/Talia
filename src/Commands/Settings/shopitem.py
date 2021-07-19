"""
Talia Discord Bot
GNU General Public License v3.0
shopitem.py (Commands/Settings)

shopitem command
"""
import asyncio
from Utils import guild, message, other
from Storage import help_list

name = "shopitem"
dm_capable = False


async def run(args, bot, msg, conn, guildinfo, userinfo):
    if not msg.author.guild_permissions.manage_guild and msg.author.id not in other.load_config().owners:
        await message.send_error(msg, "You have insufficient permissions to use this command")
        return

    if len(args) < 2:
        await message.invalid_use(msg, help_list.shopitem, "No operation given")
        return

    if len(args) < 3:
        await message.invalid_use(msg, help_list.shopitem, "No name/id given")
        return

    args[1] = args[1].lower()

    if args[1] == "create":
        await _shopitem_create(args, bot, msg, conn, guildinfo)
    elif args[1] == "remove":
        await _shopitem_remove(args, msg, conn, guildinfo)
    else:
        await message.send_error(msg, f"Unknown operation: {args[1]}")


async def _shopitem_create(args, bot, msg, conn, guildinfo):
    item_name = " ".join(args[2:])

    if len(item_name) > 32:
        await message.send_error(msg, "The item name needs to be less than 32 characters")
        return

    for char in item_name:
        if ord(char) < 32 or ord(char) > 126:
            await message.send_error(msg, f"Invalid character: {char}")
            return

    if len(guildinfo.shop) >= 15:
        await message.send_error(msg, "The server has reached the maximum amount of shop items (15)")
        return

    for item in guildinfo.shop:
        if item["name"].lower() == item_name.lower():
            await message.send_error(msg, "There's already an item with that name")
            return

    sent_msg = await message.send_message(msg, f"""Item name: {item_name}
Cost: None

**How much should this item cost**""", title="New shop item")

    def msg_check(m):
        if m.author != msg.author:
            return False

        if m.channel != msg.channel:
            return False

        return True

    try:
        user_msg = await bot.wait_for("message", timeout=120, check=msg_check)
    except asyncio.TimeoutError:
        await message.edit_message(sent_msg, sent_msg.embeds[0].description, title="Timed out")
        return

    user_msg.content = user_msg.content.replace(",", "")

    try:
        cost = int(user_msg.content)
    except ValueError:
        await message.send_error(msg, "Invalid cost")
        return

    guildinfo = guild.load_guild(msg.guild.id, conn)

    if len(guildinfo.shop) >= 15:
        await message.send_error(msg, "The server has reached the maximum amount of shop items (15)")
        return

    for item in guildinfo.shop:
        if item["name"].lower() == item_name.lower():
            await message.send_error(msg, "There's already an item with that name")
            return

    guildinfo.shop.append({
        "name": item_name,
        "cost": cost
    })
    guild.set_guild_attr(msg.guild.id, "shop", guildinfo.shop, conn)

    emojis = other.load_emojis(bot)
    await message.edit_message(sent_msg, f"""Item name: {item_name}
Cost: {cost:,} {emojis.coin}""", title="Item created")


async def _shopitem_remove(args, msg, conn, guildinfo):
    try:
        item = int(args[2]) - 1
    except ValueError:
        await message.send_error(msg, "Invalid item ID")
        return

    if item < 0 or item > len(guildinfo.shop) - 1:
        await message.send_error(msg, "There's no item in the server shop with that ID")
        return

    guildinfo.shop.pop(item)
    guild.set_guild_attr(msg.guild.id, "shop", guildinfo.shop, conn)

    await message.send_message(msg, "Item removed from the server shop", title="Item removed")