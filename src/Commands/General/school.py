"""
Talia Discord Bot
GNU General Public License v3.0
school.py (Commands/General)

school command
"""
import asyncio
import discord_components
from Utils import user, timer, message, abc, other

#   Command Information   #
name = "school"
dm_capable = True
# ~~~~~~~~~~~~~~~~~~~~~~~ #

edu_levels = {
    1: {
        "name": "Elementary",
        "cost": 0,
        "time": 0
    },
    2: {
        "name": "Highschool",
        "cost": 2000,
        "time": 21600
    },
    3: {
        "name": "College",
        "cost": 30000,
        "time": 86400
    },
    4: {
        "name": "PhD",
        "cost": 100000,
        "time": 259200
    }
}


async def run(bot, msg, conn):
    school_timer = timer.load_edu_timer(msg.author.id, conn)

    if school_timer is not None:
        await message.send_error(msg, f"You're already in class for the next {timer.load_time(school_timer.time)}")
        return

    userinfo = user.load_user(msg.author.id, conn)

    if userinfo.edu_level == max(edu_levels.keys()):
        await message.send_error(msg, "You've already reached the highest education level")
        return

    emojis = other.load_emojis(bot)

    if edu_levels[userinfo.edu_level + 1]["cost"] > userinfo.coins:
        await message.send_error(msg,
            f"""You don't have enough coins to get a {edu_levels[userinfo.edu_level + 1]['name']} education level
(Costs {edu_levels[userinfo.edu_level + 1]['cost']} {emojis.coin})"""
        )
        return

    if userinfo.settings.reaction_confirm:
        sent_msg, interaction, result = await _reaction_confirm(bot, msg, userinfo, emojis)
    else:
        sent_msg, interaction, result = await _button_confirm(bot, msg, userinfo, emojis)

    if result is None:
        return

    if result == "cancel":
        await message.response_edit(sent_msg, interaction, sent_msg.embeds[0].description, title="Cancelled",
            from_reaction=userinfo.settings.reaction_confirm
        )
        return

    userinfo = user.load_user(msg.author.id, conn)
    userinfo.edu_level += 1

    if edu_levels[userinfo.edu_level]["cost"] > userinfo.coins:
        await message.response_send(sent_msg, interaction, "You no longer have enough coins",
            from_reaction=userinfo.settings.reaction_confirm
        )
        return

    school_timer = timer.load_edu_timer(msg.author.id, conn)

    if school_timer is not None:
        await message.response_send(sent_msg, interaction, "You're already in class",
            from_reaction=userinfo.settings.reaction_confirm
        )
        return

    user.set_user_attr(msg.author.id, "coins", userinfo.coins - edu_levels[userinfo.edu_level]["cost"], conn, False)
    timer.new_edu_timer(
        abc.EduTimer(msg.author.id, edu_levels[userinfo.edu_level]["time"], userinfo.edu_level),
        conn
    )

    await message.response_edit(sent_msg, interaction,
        f"""You've started your {edu_levels[userinfo.edu_level]['name']} education level
Time remaining: {timer.load_time(edu_levels[userinfo.edu_level]['time'])}""", title="Education",
        from_reaction=userinfo.settings.reaction_confirm
    )


async def _reaction_confirm(bot, msg, userinfo, emojis):
    sent_msg = await message.send_message(msg,
        f"Are you sure you want to pay {edu_levels[userinfo.edu_level + 1]['cost']} {emojis.coin} for a {edu_levels[userinfo.edu_level + 1]['name']} education level?",
        title="Education"
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


async def _button_confirm(bot, msg, userinfo, emojis):
    sent_msg = await message.send_message(msg,
        f"Are you sure you want to pay {edu_levels[userinfo.edu_level + 1]['cost']} {emojis.coin} for a {edu_levels[userinfo.edu_level + 1]['name']} education level?",
        title="Education", components=[[
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