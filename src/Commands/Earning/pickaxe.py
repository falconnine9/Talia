"""
Talia Discord Bot
GNU General Public License v3.0
pickaxe.py (Commands/Earning)

pickaxe command
"""
import asyncio
import discord_components
from Utils import user, subtable, message, abc, other
from Storage import help_list

name = "pickaxe"
dm_capable = True

_pickaxes = {
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
        "speed": 2,
        "multiplier": 1.3
    },
    4: {
        "name": "Mithril Pickaxe",
        "cost": 10000,
        "speed": 3,
        "multiplier": 1.5
    },
    5: {
        "name": "Infinity Pickaxe",
        "cost": 40000,
        "speed": 3,
        "multiplier": 1.7
    },
    6: {
        "name": "Universal Pickaxe",
        "cost": 100000,
        "speed": 4,
        "multiplier": 2
    },
    7: {
        "name": "Silver Drill",
        "cost": 500000,
        "speed": 5,
        "multiplier": 2.3
    },
    8: {
        "name": "Diamond Drill",
        "cost": 2000000,
        "speed": 5,
        "multiplier": 2.6
    },
    9: {
        "name": "TNT",
        "cost": 5000000,
        "speed": 6,
        "multiplier": 2.9
    },
    10: {
        "name": "Nuclear Explosives",
        "cost": 10000000,
        "speed": 6,
        "multiplier": 3.3
    },
    11: {
        "name": "Supernova",
        "cost": 40000000,
        "speed": 6,
        "multiplier": 3.7
    },
    12: {
        "name": "Black Hole",
        "cost": 100000000,
        "speed": 7,
        "multiplier": 4.2
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

    if pickaxe_id not in _pickaxes:
        await message.send_message(msg, "There's no pickaxe with that ID")
        return

    if _pickaxes[pickaxe_id]["cost"] > userinfo.coins:
        await message.send_error(msg, "You don't have enough coins for this pickaxe")
        return

    emojis = other.load_emojis(bot)

    if userinfo.settings.reaction_confirm:
        sent_msg, interaction, result = await _pickaxe_buy_reaction_confirm(bot, msg, pickaxe_id, emojis)
    else:
        sent_msg, interaction, result = await _pickaxe_buy_button_confirm(bot, msg, pickaxe_id, emojis)

    if result is None:
        return

    if result == "cancel":
        await message.response_edit(sent_msg, interaction, sent_msg.embeds[0].description, title="Cancelled",
            from_reaction=userinfo.settings.reaction_confirm
        )
        return

    userinfo = user.load_user(msg.author.id, conn)

    if userinfo.pickaxe is not None:
        await message.response_send(sent_msg, interaction, "You already have a pickaxe equipped",
            from_reaction=userinfo.settings.reaction_confirm
        )
        return

    if _pickaxes[pickaxe_id]["cost"] > userinfo.coins:
        await message.response_send(sent_msg, interaction, "You no longer have enough coins",
            from_reaction=userinfo.settings.reaction_confirm
        )
        return

    user.set_user_attr(msg.author.id, "coins", userinfo.coins - _pickaxes[pickaxe_id]["cost"], conn, False)
    subtable.new_pickaxe(msg.author.id, abc.Pickaxe(
        _pickaxes[pickaxe_id]["name"], _pickaxes[pickaxe_id]["cost"],
        _pickaxes[pickaxe_id]["speed"], _pickaxes[pickaxe_id]["multiplier"]
    ), conn)

    await message.response_edit(sent_msg, interaction,
        f"You bought a {_pickaxes[pickaxe_id]['name']} for {_pickaxes[pickaxe_id]['cost']:,} {emojis.coin}",
        title="Bought", from_reaction=userinfo.settings.reaction_confirm
    )


async def _pickaxe_sell(bot, msg, conn):
    userinfo = user.load_user(msg.author.id, conn)

    if userinfo.pickaxe is None:
        await message.send_error(msg, "You don't have a pickaxe equipped")
        return

    sell_amount = round(userinfo.pickaxe.worth / 4)
    emojis = other.load_emojis(bot)

    if userinfo.settings.reaction_confirm:
        sent_msg, interaction, result = await _pickaxe_sell_reaction_confirm(bot, msg, userinfo, sell_amount, emojis)
    else:
        sent_msg, interaction, result = await _pickaxe_sell_button_confirm(bot, msg, userinfo, sell_amount, emojis)

    if result is None:
        return

    if result == "cancel":
        await message.response_edit(sent_msg, interaction, sent_msg.embeds[0].description, title="Cancelled",
            from_reaction=userinfo.settings.reaction_confirm
        )
        return

    userinfo = user.load_user(msg.author.id, conn)

    if userinfo.pickaxe is None:
        await message.response_send(sent_msg, interaction, "You no longer have a pickaxe equipped",
            from_reaction=userinfo.settings.reaction_confirm
        )
        return

    sell_amount = round(userinfo.pickaxe.worth / 4)

    user.set_user_attr(msg.author.id, "coins", userinfo.coins + sell_amount, conn, False)
    subtable.remove_pickaxe(msg.author.id, conn)

    await message.response_edit(sent_msg, interaction,
        f"You sold your {userinfo.pickaxe.name} for {sell_amount:,} {emojis.coin}", title="Sold",
        from_reaction=userinfo.settings.reaction_confirm
    )


async def _pickaxe_list(bot, msg):
    fields = []
    emojis = other.load_emojis(bot)

    for pickaxe in _pickaxes.keys():
        fields.append([_pickaxes[pickaxe]["name"], f"""ID: {pickaxe}
Cost: {_pickaxes[pickaxe]['cost']:,} {emojis.coin}
Mining Speed: {_pickaxes[pickaxe]['speed']}
Mining Multiplier: x{_pickaxes[pickaxe]['multiplier']}"""])

    await message.send_message(msg, title="Pickaxes", fields=fields)


async def _pickaxe_buy_reaction_confirm(bot, msg, pickaxe_id, emojis):
    sent_msg = await message.send_message(msg,
        f"Are you sure you want to buy a {_pickaxes[pickaxe_id]['name']} for {_pickaxes[pickaxe_id]['cost']:,} {emojis.coin}",
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


async def _pickaxe_buy_button_confirm(bot, msg, pickaxe_id, emojis):
    sent_msg = await message.send_message(msg,
        f"Are you sure you want to buy a {_pickaxes[pickaxe_id]['name']} for {_pickaxes[pickaxe_id]['cost']:,} {emojis.coin}",
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


async def _pickaxe_sell_reaction_confirm(bot, msg, userinfo, sell_amount, emojis):
    sent_msg = await message.send_message(msg,
        f"Are you sure you want to sell your {userinfo.pickaxe.name} for {sell_amount:,} {emojis.coin}",
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
        await message.timeout_response(sent_msg)
        return None, None, None

    if str(reaction.emoji) == "\u2705":
        return sent_msg, None, "confirm"
    else:
        return sent_msg, None, "cancel"


async def _pickaxe_sell_button_confirm(bot, msg, userinfo, sell_amount, emojis):
    sent_msg = await message.send_message(msg,
        f"Are you sure you want to sell your {userinfo.pickaxe.name} for {sell_amount:,} {emojis.coin}",
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