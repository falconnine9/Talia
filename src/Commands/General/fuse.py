"""
Talia Discord Bot
GNU General Public License v3.0
fuse.py (Commands/General)

fuse command
"""
import asyncio
import discord_components
from Utils import user, message

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

    sent_msg = await message.send_message(msg, f"""Are you sure you want to upgrade to {fusion_levels[userinfo.fusion_level + 1]} fusion

You will become Level 1, and have a multiplier of x1.0""", title="Fusion..",
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

    if userinfo.fusion_level >= 8:
        await message.edit_message(sent_msg, sent_msg.embeds[0].description, title="Fusion..", components=[])
        await message.send_error(msg, "You've already reached Hydra fusion")
        return

    if userinfo.level < 40:
        await message.edit_message(sent_msg, sent_msg.embeds[0].description, title="Fusion..", components=[])
        await message.send_error(msg, "You no longer have the required level to fuse")
        return

    user.set_user_attr(msg.author.id, "xp", 0, conn, False)
    user.set_user_attr(msg.author.id, "level", 1, conn, False)
    user.set_user_attr(msg.author.id, "multiplier", 1.0, conn, False)
    user.set_user_attr(msg.author.id, "fusion_level", userinfo.fusion_level + 1, conn)

    await message.edit_message(sent_msg, f"You upgrade to {fusion_levels[userinfo.fusion_level + 1]} fusion", title="Fused", components=[])