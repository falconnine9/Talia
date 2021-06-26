"""
Talia Discord Bot
GNU General Public License v3.0
fuse.py (Commands/General)

fuse command
"""
import asyncio
import discord_components
from Utils import user, message

#   Command Information   #
name = "fuse"
dm_capable = True
# ~~~~~~~~~~~~~~~~~~~~~~~ #

fusion_levels = {
    1: "Human",
    2: "Tiger",
    3: "Minotaur",
    4: "Gryphon",
    5: "Elephant",
    6: "Reaper",
    7: "Dragon",
    8: "Hydra"
}


async def run(bot, msg, conn):
    userinfo = user.load_user(msg.author.id, conn)

    if userinfo.level < 40:
        await message.send_error(msg, "You gave to be at least level 40 to fuse")
        return

    if userinfo.fusion_level >= 8:
        await message.send_error(msg, "You've already reached Hydra fusion")
        return

    if userinfo.settings.reaction_confirm:
        sent_msg, interaction, result = await _reaction_confirm(bot, msg, userinfo)
    else:
        sent_msg, interaction, result = await _button_confirm(bot, msg, userinfo)

    if result is None:
        return

    if result == "cancel":
        await message.response_edit(sent_msg, interaction, sent_msg.embeds[0].description, title="Cancelled",
            from_reaction=userinfo.settings.reaction_confirm
        )
        return

    userinfo = user.load_user(msg.author.id, conn)

    if userinfo.fusion_level >= 8:
        await message.response_send(sent_msg, interaction, "You've already reached Hydra fusion",
            from_reaction=userinfo.settings.reaction_confirm
        )
        return

    if userinfo.level < 40:
        await message.response_send(sent_msg, interaction, "You no longer have the required level to fuse",
            from_reaction=userinfo.settings.reaction_confirm
        )
        return

    user.set_user_attr(msg.author.id, "xp", 0, conn, False)
    user.set_user_attr(msg.author.id, "level", 1, conn, False)
    user.set_user_attr(msg.author.id, "multiplier", 1.0, conn, False)
    user.set_user_attr(msg.author.id, "fusion_level", userinfo.fusion_level + 1, conn)

    await message.response_edit(sent_msg, interaction,
        f"You upgraded to {fusion_levels[userinfo.fusion_level + 1]} fusion", title="Fused",
        from_reaction=userinfo.settings.reaction_confirm
    )


async def _reaction_confirm(bot, msg, userinfo):
    sent_msg = await message.send_message(msg,
        f"""Are you sure you want to upgrade to {fusion_levels[userinfo.fusion_level + 1]} fusion

You will become Level 1, and have a multiplier of x1.0""", title="Fusion.."
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


async def _button_confirm(bot, msg, userinfo):
    sent_msg = await message.send_message(msg,
        f"""Are you sure you want to upgrade to {fusion_levels[userinfo.fusion_level + 1]} fusion

You will become Level 1, and have a multiplier of x1.0""", title="Fusion..", components=[[
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