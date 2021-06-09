"""
Talia Discord Bot
GNU General Public License v3.0
hourly.py (Commands/Earning)

hourly command
"""
import random
from Utils import user, timer, message, abc, other


async def run(bot, msg, conn):
    hourly_timer = timer.load_timer(f"hourly.{msg.author.id}", conn)

    if hourly_timer is not None:
        await message.send_error(msg, f"Wait {timer.load_time(hourly_timer.time)} before collecting your next hourly")
        return

    userinfo = user.load_user(msg.author.id, conn)
    earned_coins = round(random.randint(10, 50) * other.load_multi(userinfo, conn))
    earned_xp = round(random.randint(1, 15) * other.load_multi(userinfo, conn))

    user.set_user_attr(msg.author.id, "coins", userinfo.coins + earned_coins, conn, False)
    user.set_user_attr(msg.author.id, "xp", userinfo.xp + earned_xp, conn, False)
    user.set_user_attr(msg.author.id, "hourly", userinfo.hourly + 1, conn, False)

    daily_timer = abc.Timer(f"hourly.{msg.author.id}", 3600, msg.author.id, None)
    timer.new_timer(daily_timer, conn)

    emojis = other.load_emojis(bot)

    await message.send_message(msg, f"""+{earned_coins} {emojis.coin}
+{earned_xp} XP

**You've collected {userinfo.hourly + 1} hourlies**""", title="Hourly")