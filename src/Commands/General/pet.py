"""
Talia Discord Bot
GNU General Public License v3.0
pet.py (Commands/General)

pet command
"""
import asyncio
import discord_components
import random
from Utils import user, subtable, message, abc, other
from Storage import help_list

name = "pet"
dm_capable = True

_pets = {
    "dog": {
        "cost": 500,
        "breeds": [
            "German Shepard",
            "Poodle",
            "Golden Retriever",
            "Chihuahua",
            "French Bulldog",
            "Pomeranian",
            "Bulldog",
            "Great Dane",
            "Husky",
            "Rottweiler",
            "Greyhound",
            "Maltese",
            "Shiba Inu",
            "Havanese",
            "Labradoodle"
        ]
    },
    "horse": {
        "cost": 500,
        "breeds": [
            "Arabian",
            "Thoroughbred",
            "Appaloosa"
            "Morgan",
            "Pony"
        ]
    },
    "cat": {
        "cost": 500,
        "breeds": [
            "British Shorthair",
            "Maine Coon",
            "Sphynx",
            "American Shorthair",
            "Ragdoll",
            "Scottish Fold",
            "Birman",
            "Japanese Bobtail",
            "Oriental Shorthair",
            "American Bobtail",
            "Ragamuffin",
            "Egyptian Mau",
            "Chartreux",
            "Korat",
            "Turkish Van",
            "Havana Brown"
        ]
    },
    "parrot": {
        "cost": 500,
        "breeds": [
            "African Grey",
            "Eclectus",
            "Cockatoo",
            "Macaw"
        ]
    }
}
_default_names = [
    "Abel",
    "Bella",
    "Charlie",
    "Luna",
    "Lucy",
    "Max",
    "Baily",
    "Cooper",
    "Daisy"
]


async def run(args, bot, msg, conn):
    if len(args) < 2:
        await message.invalid_use(msg, help_list.pet, "No operation given")
        return

    args[1] = args[1].lower()

    if args[1] == "buy":
        await _pet_buy(bot, msg, conn, args)
    elif args[1] == "sell":
        await _pet_sell(bot, msg, conn)
    elif args[1] == "list":
        await _pet_list(bot, msg)
    elif args[1] == "name":
        await _pet_name(msg, conn, args)
    else:
        await message.send_error(msg, f"Unknown operation: {args[1]}")


async def _pet_buy(bot, msg, conn, args):
    if len(args) < 3:
        await message.invalid_use(msg, help_list.pet, "No pet name given")
        return

    userinfo = user.load_user(msg.author.id, conn)
    args[2] = args[2].lower()

    if userinfo.pet is not None:
        await message.send_error(msg, "You already have a pet\nSell it to buy a new one")
        return

    if args[2] not in _pets:
        await message.send_error(msg, "No pet found")
        return

    if _pets[args[2]]["cost"] > userinfo.coins:
        await message.send_error(msg, "You don't have enough coins to buy this pet")
        return

    emojis = other.load_emojis(bot)

    if userinfo.settings.reaction_confirm:
        sent_msg, interaction, result = await _pet_buy_reaction_confirm(bot, msg, args, emojis)
    else:
        sent_msg, interaction, result = await _pet_buy_button_confirm(bot, msg, args, emojis)

    if result is None:
        return

    if result == "cancel":
        await message.response_edit(sent_msg, interaction, sent_msg.embeds[0].description, title="Cancelled",
            from_reaction=userinfo.settings.reaction_confirm
        )
        return

    userinfo = user.load_user(msg.author.id, conn)

    if userinfo.pet is not None:
        await message.response_send(sent_msg, interaction, "You already have a pet",
            from_reaction=userinfo.settings.reaction_confirm
        )
        return

    if _pets[args[2]]["cost"] > userinfo.coins:
        await message.response_send(sent_msg, interaction, "You no longer have enough coins to buy this pet",
            from_reaction=userinfo.settings.reaction_confirm
        )
        return

    def_name = random.choice(_default_names)
    breed = random.choice(_pets[args[2]]["breeds"])

    user.set_user_attr(msg.author.id, "coins", userinfo.coins - _pets[args[2]]["cost"], conn, False)
    subtable.new_pet(msg.author.id, abc.Pet(
        def_name, _pets[args[2]]["cost"],
        f"{args[2][0].upper()}{args[2][1:].lower()}",
        breed
    ), conn)

    await message.response_edit(sent_msg, interaction, f"""You bought a pet!
Your pet is a {breed} ({args[2][0].upper()}{args[2][1:].lower()})
By default is has the name **{def_name}**. But that can be changed with `pet name`""", title="Bought",
        from_reaction=userinfo.settings.reaction_confirm
    )


async def _pet_sell(bot, msg, conn):
    userinfo = user.load_user(msg.author.id, conn)

    if userinfo.pet is None:
        await message.send_error(msg, "You don't have a pet to sell")
        return

    emojis = other.load_emojis(bot)

    if userinfo.settings.reaction_confirm:
        sent_msg, interaction, result = await _pet_sell_reaction_confirm(bot, msg, userinfo, emojis)
    else:
        sent_msg, interaction, result = await _pet_sell_button_confirm(bot, msg, userinfo, emojis)

    if result is None:
        return

    if result == "cancel":
        await message.response_edit(sent_msg, interaction, sent_msg.embeds[0].description, title="Cancelled",
            from_reaction=userinfo.settings.reaction_confirm
        )
        return

    userinfo = user.load_user(msg.author.id, conn)

    if userinfo.pet is None:
        await message.response_send(sent_msg, interaction, "You don't have a pet",
            from_reaction=userinfo.settings.reaction_confirm
        )
        return

    user.set_user_attr(msg.author.id, "coins", userinfo.coins + userinfo.pet.worth, conn, False)
    subtable.remove_pet(msg.author.id, conn)

    await message.response_edit(sent_msg, interaction, f"You sold your pet for {userinfo.pet.worth:,} {emojis.coin}",
        title="Sold", from_reaction=userinfo.settings.reaction_confirm
    )


async def _pet_list(bot, msg):
    fields = []
    emojis = other.load_emojis(bot)

    for pet in _pets.keys():
        fields.append([f"{pet[0].upper()}{pet[1:]}", f"Cost: {_pets[pet]['cost']:,} {emojis.coin}"])

    await message.send_message(msg, title="Pets", fields=fields, footer="(Pets are still in beta phase)")


async def _pet_name(msg, conn, args):
    if len(args) < 3:
        await message.invalid_use(msg, help_list.pet, "No pet name given")
        return

    userinfo = user.load_user(msg.author.id, conn)

    if userinfo.pet is None:
        await message.send_error(msg, "You don't have a pet")
        return

    pet_name = " ".join(args[2:])

    if len(pet_name) > 32:
        await message.send_error(msg, "The name must be less than 32 characters")
        return

    if pet_name == userinfo.pet.name:
        await message.send_error(msg, "That's already your pet's name")
        return

    subtable.set_pet_attr(msg.author.id, "name", pet_name, conn)
    await message.send_message(msg, f"You changed your pet's name to **{pet_name}**", title="Renamed")


async def _pet_buy_reaction_confirm(bot, msg, args, emojis):
    sent_msg = await message.send_message(msg,
        f"Are you sure you want to buy a {args[2][0].upper()}{args[2][1:]} for {_pets[args[2]]['cost']:,} {emojis.coin}",
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


async def _pet_buy_button_confirm(bot, msg, args, emojis):
    sent_msg = await message.send_message(msg,
        f"Are you sure you want to buy a {args[2][0].upper()}{args[2][1:]} for {_pets[args[2]]['cost']:,} {emojis.coin}",
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


async def _pet_sell_reaction_confirm(bot, msg, userinfo, emojis):
    sent_msg = await message.send_message(msg,
        f"Are you sure you want to sell your pet for {userinfo.pet.worth:,} {emojis.coin}", title="Selling.."
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


async def _pet_sell_button_confirm(bot, msg, userinfo, emojis):
    sent_msg = await message.send_message(msg,
        f"Are you sure you want to sell your pet for {userinfo.pet.worth:,} {emojis.coin}", title="Selling..",
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