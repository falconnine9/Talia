import asyncio
from Utils import user, message, abc, other
from Storage import help_list


pickaxes = {
    1: {
        "name": "Bronze Pickaxe",
        "cost": 150,
        "speed": 1,
        "multiplier": 1.0
    },
    2: {
        "name": "Steel Pickaxe",
        "cost": 800,
        "speed": 2,
        "multiplier": 1.1
    },
    3: {
        "name": "Laser Pickaxe",
        "cost": 3000,
        "speed": 3,
        "multiplier": 1.3
    },
    4: {
        "name": "Mithril Pickaxe",
        "cost": 10000,
        "speed": 4,
        "multiplier": 1.5
    },
    5: {
        "name": "Infinity Pickaxe",
        "cost": 40000,
        "speed": 5,
        "multiplier": 1.7
    },
    6: {
        "name": "Universal Pickaxe",
        "cost": 100000,
        "speed": 6,
        "multiplier": 2
    }
}


async def run(bot, msg, conn):
    split_data = msg.content.split(" ")

    if len(split_data) < 2:
        await message.invalid_use(msg, help_list.pickaxe, "No operation given")
        return

    split_data[1] = split_data[1].lower()

    if split_data[1] == "buy":
        await _pickaxe_buy(bot, msg, conn, split_data)

    elif split_data[1] == "sell":
        await _pickaxe_sell(bot, msg, conn)

    elif split_data[1] == "list":
        await _pickaxe_list(bot, msg)

    else:
        await message.send_error(msg, f"Unknown operation: {split_data[1]}")


async def _pickaxe_buy(bot, msg, conn, split_data):
    if len(split_data) < 3:
        await message.invalid_use(msg, help_list.pickaxe, "No pickaxe given")
        return

    userinfo = user.load_user(msg.author.id, conn)

    if userinfo.pickaxe is not None:
        await message.send_error(msg, "You already have a pickaxe")
        return

    try:
        pickaxe_id = int(split_data[2])
    except ValueError:
        await message.send_error(msg, "Invalid pickaxe ID")
        return

    if pickaxe_id not in pickaxes:
        await message.send_message(msg, "There's no pickaxe with that ID")
        return

    if pickaxes[pickaxe_id]["cost"] > userinfo.coins:
        await message.send_error(msg, "You don't have enough coins for this pickaxe")
        return

    emojis = other.load_emojis(bot)
    sent_msg = await message.send_message(msg, f"Are you sure you want to buy a {pickaxes[pickaxe_id]['name']} for {pickaxes[pickaxe_id]['cost']} {emojis.coin}", title="Buying..")

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

    if userinfo.pickaxe is not None:
        await message.send_error(msg, "You already have a pickaxe equipped")
        return

    if pickaxes[pickaxe_id]["cost"] > userinfo.coins:
        await message.send_error(msg, "You no longer have enough coins")
        return

    user.set_user_attr(msg.author.id, "pickaxe", abc.Pickaxe(
        pickaxes[pickaxe_id]["name"],
        pickaxes[pickaxe_id]["cost"],
        0, 1,
        pickaxes[pickaxe_id]["speed"],
        pickaxes[pickaxe_id]["multiplier"]
    ).cvt_dict(), conn)
    await message.edit_message(sent_msg, f"You bought a {pickaxes[pickaxe_id]['name']} for {pickaxes[pickaxe_id]['cost']} {emojis.coin}", title="Bought")


async def _pickaxe_sell(bot, msg, conn):
    userinfo = user.load_user(msg.author.id, conn)

    if userinfo.pickaxe is None:
        await message.send_error(msg, "You don't have a pickaxe equipped")
        return

    sell_amount = round(userinfo.pickaxe.worth / 4)
    emojis = other.load_emojis(bot)
    sent_msg = await message.send_message(msg, f"Are you sure you want to sell your {userinfo.pickaxe.name} for {sell_amount} {emojis.coin}", title="Selling..")

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

    if userinfo.pickaxe is None:
        await message.send_error(msg, "You no longer have a pickaxe equipped")
        return

    sell_amount = round(userinfo.pickaxe.worth / 4)

    user.set_user_attr(msg.author.id, "coins", userinfo.coins + sell_amount, conn, False)
    user.set_user_attr(msg.author.id, "pickaxe", None, conn)

    await message.edit_message(sent_msg, f"You sold your {userinfo.pickaxe.name} for {sell_amount}", title="Sold")


async def _pickaxe_list(bot, msg):
    fields = []
    emojis = other.load_emojis(bot)

    for pickaxe in pickaxes.keys():
        fields.append([pickaxes[pickaxe]["name"], f"""ID: {pickaxe}
Cost: {pickaxes[pickaxe]['cost']} {emojis.coin}
Mining Speed: {pickaxes[pickaxe]['speed']}
Mining Multiplier: x{pickaxes[pickaxe]['multiplier']}"""])

    await message.send_message(msg, title="Pickaxes", fields=fields)