import asyncio

from Utils import user, timer, message, abc, other

edu_levels = {
    1: {
        "name": "Elementary",
        "cost": 0,
        "time": 0
    },
    2: {
        "name": "Highschool",
        "cost": 1000,
        "time": 21600
    },
    3: {
        "name": "College",
        "cost": 4000,
        "time": 86400
    },
    4: {
        "name": "PhD",
        "cost": 10000,
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
        await message.send_error(msg, f"""You don't have enough coins to get a {edu_levels[userinfo.edu_level + 1]['name']} education level
(Costs {edu_levels[userinfo.edu_level + 1]['cost']} {emojis.coin})""")
        return

    sent_msg = await message.send_message(msg, f"Are you sure you want to pay {edu_levels[userinfo.edu_level + 1]['cost']} {emojis.coin} for a {edu_levels[userinfo.edu_level + 1]['name']} education level?", title="Education")

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
    userinfo.edu_level += 1

    if edu_levels[userinfo.edu_level]["cost"] > userinfo.coins:
        await message.send_error(msg, "You no longer have enough coins")
        return

    school_timer = timer.load_edu_timer(msg.author.id, conn)

    if school_timer is not None:
        await message.send_error(msg, "You're already in class")
        return

    user.set_user_attr(msg.author.id, "coins", userinfo.coins - edu_levels[userinfo.edu_level]["cost"], conn, False)
    timer.new_edu_timer(
        abc.EduTimer(msg.author.id, edu_levels[userinfo.edu_level]["time"], userinfo.edu_level),
        conn
    )

    await message.edit_message(sent_msg, f"""You've started your {edu_levels[userinfo.edu_level]['name']} education level
Time remaining: {timer.load_time(edu_levels[userinfo.edu_level]['time'])}""", title="Education")