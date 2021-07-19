"""
Talia Discord Bot
GNU General Public License v3.0
daily.py (Commands/Earning)

daily command
"""
import random
from Utils import user, timer, message, abc, other

name = "daily"
dm_capable = True


async def run(args, bot, msg, conn, guildinfo, userinfo):
    daily_timer = timer.load_timer(f"daily.{msg.author.id}", conn)

    if daily_timer is not None:
        await message.send_error(msg, f"Wait {timer.load_time(daily_timer.time)} before collecting your next daily")
        return

    earned_coins = round(random.randint(30, 500) * other.load_multi(userinfo, conn))
    earned_xp = round(random.randint(5, 30) * other.load_multi(userinfo, conn))

    user.set_user_attr(msg.author.id, "coins", userinfo.coins + earned_coins, conn, False)
    user.set_user_attr(msg.author.id, "xp", userinfo.xp + earned_xp, conn, False)
    user.set_user_attr(msg.author.id, "daily", userinfo.daily + 1, conn, False)

    daily_timer = abc.Timer(f"daily.{msg.author.id}", 86400, msg.author.id, None)
    timer.new_timer(daily_timer, conn)

    emojis = other.load_emojis(bot)

    await message.send_message(msg, f"""+{earned_coins:,} {emojis.coin}
+{earned_xp:,} XP

**You've collected {userinfo.daily + 1} dailies**""", title="Daily")