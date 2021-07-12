"""
Talia Discord Bot
GNU General Public License v3.0
post_checks.py (Routine)

Checks that will occur after every command is run
"""
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
    30: "Gold",
    70: "Titanium",
    150: "Celestial",
    250: "Titan",
    500: "wtf"
}


async def level(bot, msg, conn):
    userinfo = user.load_user(msg.author.id, conn)

    if userinfo.xp >= userinfo.level * 25:
        user.set_user_attr(msg.author.id, "level", userinfo.level + 1, conn, False)
        user.set_user_attr(msg.author.id, "xp", 0, conn, False)
        user.set_user_attr(msg.author.id, "multiplier", round(userinfo.multiplier + 0.1, 1), conn)

        emojis = other.load_emojis(bot)
        await message.send_message(msg,
            f"""{emojis.confetti} {str(msg.author)} reached level {userinfo.level + 1} {emojis.confetti}
Base Multiplier: x{userinfo.multiplier} -> x{round(userinfo.multiplier + 0.1, 1)}""", title="Level up"
        )


async def achievements(bot, msg, conn):
    userinfo = user.load_user(msg.author.id, conn)

    for milestone in money_achievements:
        if milestone > userinfo.coins:
            break

        if money_achievements[milestone] in userinfo.achievements:
            continue

        userinfo.achievements.append(money_achievements[milestone])

        emojis = other.load_emojis(bot)
        await message.send_message(msg,
            f"{emojis.confetti} {str(msg.author)} earned the {money_achievements[milestone]} achievement {emojis.confetti}",
            title="Achievement"
        )
        break

    for milestone in level_achievements:
        if milestone > userinfo.level:
            break

        if level_achievements[milestone] in userinfo.achievements:
            continue

        userinfo.achievements.append(level_achievements[milestone])

        emojis = other.load_emojis(bot)
        await message.send_message(msg,
            f"{emojis.confetti} {str(msg.author)} earned the {level_achievements[milestone]} achievement {emojis.confetti}",
            title="Achievement"
        )
        break

    user.set_user_attr(msg.author.id, "achievements", userinfo.achievements, conn)