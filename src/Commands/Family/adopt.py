"""
Talia Discord Bot
GNU General Public License v3.0
adopt.py (Commands/Family)

adopt command
"""
import asyncio
import discord
import discord_components
import random
from Utils import user, message, other
from Storage import help_list

name = "adopt"
dm_capable = False

_partner_adopt = [
    "{user} is your partner",
    "You can't adopt your partner",
    "I don't think you're allowed to adopt your partner"
]
_parent_adopt = [
    "{user} is your parent",
    "Um.. {user} is your parent",
    "You can't adopt your parent"
]


async def run(bot, msg, conn):
    userinfo = user.load_user(msg.author.id, conn)

    if len(userinfo.children) >= 10:
        await message.send_error(msg, "You can only have 10 children at most")
        return

    split_data = msg.content.split(" ")

    if len(split_data) < 2:
        await message.invalid_use(msg, help_list.adopt, "No user given")
        return

    split_data[1] = split_data[1].replace("<@", "").replace("!", "").replace(">", "")

    try:
        person_id = int(split_data[1])
    except ValueError:
        await message.send_error(msg, "Invalid user")
        return

    if person_id == msg.author.id:
        await message.send_error(msg, "You can't adopt yourself")
        return
    else:
        try:
            person = await user.load_user_obj(bot, int(split_data[1]))
        except discord.NotFound:
            await message.send_error(msg, "I can't find that person")
            return
        except discord.HTTPException:
            await message.send_error(msg, "An error occurred and the command couldn't be run")
            return

    if person.bot:
        await message.send_error(msg, "You can't adopt a bot")
        return

    if person.id == userinfo.partner:
        await message.send_error(msg, random.choice(_partner_adopt).replace("{user}", str(person)))
        return

    if person.id in userinfo.parents:
        await message.send_error(msg, random.choice(_parent_adopt).replace("{user}", str(person)))
        return

    if person.id in userinfo.children:
        await message.send_error(msg, f"{str(person)} is already your child")
        return

    personinfo = user.load_user(person.id, conn)

    if len(personinfo.parents) != 0:
        await message.send_error(msg, f"{str(person)} already has parents")
        return

    if personinfo.settings.reaction_confirm:
        sent_msg, interaction, result = await _reaction_confirm(bot, msg, person)
    else:
        sent_msg, interaction, result = await _button_confirm(bot, msg, person)

    if result is None:
        return

    if result == "decline":
        await message.response_edit(sent_msg, interaction, sent_msg.embeds[0].description, title="Declined",
            from_reaction=personinfo.settings.reaction_confirm
        )
        return

    userinfo = user.load_user(msg.author.id, conn)
    personinfo = user.load_user(person.id, conn)

    if len(userinfo.children) >= 10:
        await message.response_send(sent_msg, interaction, f"{str(msg.author)} already has the maximum of 10 children",
            from_reaction=personinfo.settings.reaction_confirm
        )
        return

    if len(personinfo.parents) != 0:
        await message.response_send(sent_msg, interaction, f"You already have parents",
            from_reaction=personinfo.settings.reaction_confirm
        )
        return

    if msg.author.id in personinfo.children:
        await message.response_send(sent_msg, interaction, f"{str(msg.author)} is your child",
            from_reaction=personinfo.settings.reaction_confirm
        )
        return

    userinfo.children.append(person.id)
    user.set_user_attr(msg.author.id, "children", userinfo.children, conn, False)

    if userinfo.partner is not None:
        partnerinfo = user.load_user(userinfo.partner, conn)
        partnerinfo.children.append(person.id)
        user.set_user_attr(partnerinfo.id, "children", partnerinfo.children, conn, False)
        user.set_user_attr(person.id, "parents", [msg.author.id, partnerinfo.id], conn)

    else:
        user.set_user_attr(person.id, "parents", [msg.author.id], conn)

    emojis = other.load_emojis(bot)
    await message.response_edit(sent_msg, interaction,
        f"{emojis.confetti} {str(person)} is now the child of {str(msg.author)} {emojis.confetti}", title="Adopted",
        from_reaction=personinfo.settings.reaction_confirm
    )


async def _reaction_confirm(bot, msg, person):
    sent_msg = await message.send_message(msg, f"{str(msg.author)} wants to adopt {str(person)}", title="Adoption..")

    await sent_msg.add_reaction("\u2705")
    await sent_msg.add_reaction("\u274c")

    def reaction_check(reaction, reaction_user):
        if reaction_user != person:
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
        return sent_msg, None, "accept"
    else:
        return sent_msg, None, "decline"


async def _button_confirm(bot, msg, person):
    sent_msg = await message.send_message(msg, f"{str(msg.author)} wants to adopt {str(person)}", title="Adoption..",
        components=[[
            discord_components.Button(label="Accept", style=discord_components.ButtonStyle.green),
            discord_components.Button(label="Decline", style=discord_components.ButtonStyle.red)
        ]]
    )

    def button_check(interaction):
        if interaction.author != person:
            return False

        if interaction.message != sent_msg:
            return False

        return True

    try:
        interaction = await bot.wait_for("button_click", timeout=120, check=button_check)
    except asyncio.TimeoutError:
        await message.timeout_response(sent_msg)
        return None, None, None

    if interaction.component.label == "Accept":
        return sent_msg, interaction, "accept"
    else:
        return sent_msg, interaction, "decline"