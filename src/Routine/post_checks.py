import discord

from Utils import user, message, other

money_achievements = {
    1000: "Thousandaire",
    10000: "Ten-Thousandaire",
    100000: "Hundred-Thousandaire",
    1000000: "Millionaire",
    10000000: "Ten-Millionaire",
    100000000: "Hundred-Millionaire",
    1000000000: "Billionaire",
    10000000000: "Ten-Billionaire",
    100000000000: "Hundred-Billionaire",
    1000000000000: "Trillionaire"
}

level_achievements = {
    5: "Rookie",
    15: "Silver",
    40: "Gold",
    80: "Titanium",
    200: "Celestial",
    400: "Titan"
}


async def level(bot, msg, conn):
    userinfo = user.load_user(msg.author.id, conn)

    if userinfo.xp >= userinfo.level * (userinfo.fusion_level * 25):
        user.set_user_attr(msg.author.id, "level", userinfo.level + 1, conn, False)
        user.set_user_attr(msg.author.id, "xp", 0, conn, False)
        user.set_user_attr(msg.author.id, "multiplier", 1 + (userinfo.fusion_level * ((userinfo.level + 1) / 10)), conn)

        emojis = other.load_emojis(bot)
        await message.send_message(msg, f"{emojis.confetti} {str(msg.author)} reached level {userinfo.level + 1} {emojis.confetti}", title="Level up")

        if userinfo.level + 1 == 40:
            try:
                await message.send_message(None, "You've reached level 40, you can fuse with the `fuse` command", channel=msg.author)
            except discord.Forbidden:
                pass


async def achievements(bot, msg, conn):
    userinfo = user.load_user(msg.author.id, conn)

    for milestone in money_achievements:
        if milestone > userinfo.coins:
            break

        if money_achievements[milestone] in userinfo.achievements:
            continue

        userinfo.achievements.append(money_achievements[milestone])

        emojis = other.load_emojis(bot)
        await message.send_message(msg, f"{emojis.confetti} {str(msg.author)} earned the {money_achievements[milestone]} achievement {emojis.confetti}", title="Achievement")

    for milestone in level_achievements:
        if milestone > userinfo.level:
            break

        if level_achievements[milestone] in userinfo.achievements:
            continue

        userinfo.achievements.append(level_achievements[milestone])

        emojis = other.load_emojis(bot)
        await message.send_message(msg, f"{emojis.confetti} {str(msg.author)} earned the {level_achievements[milestone]} achievement {emojis.confetti}", title="Achievement")

    user.set_user_attr(msg.author.id, "achievements", userinfo.achievements, conn)