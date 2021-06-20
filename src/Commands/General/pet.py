"""
Talia Discord Bot
GNU General Public License v3.0
pet.py (Commands/General)

pet command
"""
import asyncio
import discord_components
import random
from Utils import user, message, abc, other
from Storage import help_list

pets = {
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

default_names = [
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


async def run(bot, msg, conn):
    split_data = msg.content.split(" ")

    if len(split_data) < 2:
        await message.invalid_use(msg, help_list.pet, "No operation given")
        return

    split_data[1] = split_data[1].lower()

    if split_data[1] == "buy":
        await _pet_buy(bot, msg, conn, split_data)

    elif split_data[1] == "sell":
        await _pet_sell(bot, msg, conn)

    elif split_data[1] == "list":
        await _pet_list(bot, msg)

    elif split_data[1] == "name":
        await _pet_name(msg, conn, split_data)

    else:
        await message.send_error(msg, f"Unknown operation: {split_data[1]}")


async def _pet_buy(bot, msg, conn, split_data):
    if len(split_data) < 3:
        await message.invalid_use(msg, help_list.pet, "No pet name given")
        return

    userinfo = user.load_user(msg.author.id, conn)
    split_data[2] = split_data[2].lower()

    if userinfo.pet is not None:
        await message.send_error(msg, "You already have a pet\nSell it to buy a new one")
        return

    if split_data[2] not in pets:
        await message.send_error(msg, "No pet found")
        return

    if pets[split_data[2]]["cost"] > userinfo.coins:
        await message.send_error(msg, "You don't have enough coins to buy this pet")
        return

    emojis = other.load_emojis(bot)
    sent_msg = await message.send_message(msg, f"Are you sure you want to buy a {split_data[2][0].upper()}{split_data[2][1:]} for {pets[split_data[2]]['cost']} {emojis.coin}", title="Buying..",
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
        return

    if interaction.component.label == "Cancel":
        await message.response_edit(sent_msg, interaction, sent_msg.embeds[0].description, title="Cancelled")
        return

    userinfo = user.load_user(msg.author.id, conn)

    if userinfo.pet is not None:
        await message.response_send(sent_msg, interaction, "You already have a pet")
        return

    if pets[split_data[2]]["cost"] > userinfo.coins:
        await message.response_send(sent_msg, interaction, "You no longer have enough coins to buy this pet")
        return

    def_name = random.choice(default_names)
    breed = random.choice(pets[split_data[2]]["breeds"])

    user.set_user_attr(msg.author.id, "coins", userinfo.coins - pets[split_data[2]]["cost"], conn, False)
    user.set_user_attr(msg.author.id, "pet", abc.Pet(
        def_name,
        pets[split_data[2]]["cost"],
        f"{split_data[2][0].upper()}{split_data[2][1:]}",
        breed
    ).cvt_dict(), conn)

    await message.response_edit(sent_msg, interaction, f"""You bought a pet!
Your pet is a {breed} ({split_data[2][0].upper()}{split_data[2][1:]})
By default is has the name **{def_name}**. But that can be changed with `pet name`""", title="Bought")


async def _pet_sell(bot, msg, conn):
    userinfo = user.load_user(msg.author.id, conn)

    if userinfo.pet is None:
        await message.send_error(msg, "You don't have a pet to sell")
        return

    emojis = other.load_emojis(bot)
    sent_msg = await message.send_message(msg, f"Are you sure you want to sell your pet for {userinfo.pet.worth} {emojis.coin}", title="Selling..",
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
        return

    if interaction.component.label == "Cancel":
        await message.response_edit(sent_msg, interaction, sent_msg.embeds[0].description, title="Cancelled")
        return

    userinfo = user.load_user(msg.author.id, conn)

    if userinfo.pet is None:
        await message.send_error(sent_msg, interaction, "You don't have a pet")
        return

    user.set_user_attr(msg.author.id, "coins", userinfo.coins + userinfo.pet.worth, conn, False)
    user.set_user_attr(msg.author.id, "pet", abc.Pet(
        None, 0, None, None
    ).cvt_dict(), conn)

    await message.response_edit(sent_msg, interaction, f"You sold your pet for {userinfo.pet.worth} {emojis.coin}", title="Sold")


async def _pet_list(bot, msg):
    fields = []
    emojis = other.load_emojis(bot)

    for pet in pets.keys():
        fields.append([f"{pet[0].upper()}{pet[1:]}", f"Cost: {pets[pet]['cost']} {emojis.coin}"])

    await message.send_message(msg, title="Pets", fields=fields, footer="(Pets are still in beta phase)")


async def _pet_name(msg, conn, split_data):
    if len(split_data) < 3:
        await message.invalid_use(msg, help_list.pet, "No pet name given")
        return

    userinfo = user.load_user(msg.author.id, conn)

    if userinfo.pet is None:
        await message.send_error(msg, "You don't have a pet")
        return

    pet_name = " ".join(split_data[2:])

    if len(pet_name) > 32:
        await message.send_error(msg, "The name must be less than 32 characters")
        return

    if pet_name == userinfo.pet.name:
        await message.send_error(msg, "That's already your pet's name")
        return

    userinfo.pet.name = pet_name
    user.set_user_attr(msg.author.id, "pet", userinfo.pet.cvt_dict(), conn)

    await message.send_message(msg, f"You changed your pet's name to **{pet_name}**", title="Renamed")