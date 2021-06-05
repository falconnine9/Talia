import asyncio

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

You will become Level 1, and have a multiplier of x1.0""", title="Fusion..")

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

    if userinfo.fusion_level >= 8:
        await message.send_error(msg, "You've already reached Hydra fusion")
        return

    if userinfo.level < 40:
        await message.send_error(msg, "You no longer have the required level to fuse")
        return

    user.set_user_attr(msg.author.id, "xp", 0, conn, False)
    user.set_user_attr(msg.author.id, "level", 1, conn, False)
    user.set_user_attr(msg.author.id, "multiplier", 1.0, conn, False)
    user.set_user_attr(msg.author.id, "fusion_level", userinfo.fusion_level + 1, conn)

    await message.edit_message(sent_msg, f"You upgrade to {fusion_levels[userinfo.fusion_level + 1]} fusion", title="Fused")