"""
Talia Discord Bot
GNU General Public License v3.0
loop.py (Routine)

Infinite loops that will run the entire time that the
 program is running
"""
import asyncio
import discord
import time
from Utils import user, message, abc, other
from Storage import meta


async def main_timer(bot, conn):
    cur = conn.cursor()
    while True:
        start_time = time.time()

        cur.execute("UPDATE timers SET time = time - 1")
        cur.execute("SELECT name, user FROM timers WHERE time <= 0 AND user IS NOT NULL")
        completed_users = cur.fetchall()

        for c_user in completed_users:
            userinfo = user.load_user(c_user[1], conn)

            if userinfo.settings.timernotifs[c_user[0].split(".")[0]]:
                bot.loop.create_task(_main_timer_alert(bot, c_user))

        cur.execute("DELETE FROM timers WHERE time <= 0")
        conn.commit()

        wait_time = time.time() - start_time

        if wait_time < 0:
            other.log(f"Main timer is {wait_time * -1} seconds behind schedule", "warning")
        else:
            await asyncio.sleep(1 - wait_time)


async def _main_timer_alert(bot, c_user):
    c_user_obj = bot.get_user(c_user[1])

    if c_user_obj is not None:
        timer_name = meta.timer_names[c_user[0].split(".")[0]]
        try:
            await message.send_message(None, f"Your {timer_name} timer has ran out", title="Timer notification",
                channel=c_user_obj
            )
        except discord.Forbidden:
            pass


async def edu_timer(bot, conn):
    cur = conn.cursor()
    while True:
        start_time = time.time()

        cur.execute("UPDATE edu_timers SET time = time - 1")
        cur.execute("SELECT * FROM edu_timers WHERE time <= 0")
        completed_users = cur.fetchall()

        for c_user in completed_users:
            user.set_user_attr(c_user[0], "edu_level", c_user[2], conn, False)
            bot.loop.create_task(_edu_timer_alert(bot, c_user, conn))

        cur.execute("DELETE FROM edu_timers WHERE time <= 0")
        conn.commit()

        wait_time = time.time() - start_time

        if wait_time < 0:
            other.log(f"Edu timer is {wait_time * -1} seconds behind schedule", "warning")
        else:
            await asyncio.sleep(1 - wait_time)


async def _edu_timer_alert(bot, c_user, conn):
    try:
        c_user_obj = await user.load_user_obj(bot, c_user[0])
    except discord.NotFound:
        return
    except discord.HTTPException:
        return

    c_userinfo = user.load_user(c_user_obj.id, conn)

    if c_userinfo is not None:
        if c_userinfo.settings.notifs["school"]:
            try:
                await message.send_message(None, "Your education level has been upgraded",
                    title="School notification", channel=c_user_obj
                )
            except discord.Forbidden:
                pass


async def invest_timer(bot, conn):
    cur = conn.cursor()
    emojis = other.load_emojis(bot)
    while True:
        start_time = time.time()

        cur.execute("UPDATE invest_timers SET time = time - 1")
        cur.execute("SELECT * FROM invest_timers WHERE time <= 0")
        completed_users = cur.fetchall()

        for c_user in completed_users:
            timerinfo = abc.InvestTimer(c_user[0], c_user[1], c_user[2], c_user[3], c_user[4], c_user[5])
            c_userinfo = user.load_user(timerinfo.id, conn)

            if c_userinfo is not None:
                if timerinfo.failed:
                    user.set_user_attr(timerinfo.id, "coins",
                        c_userinfo.coins + (round(timerinfo.coins * (1 - timerinfo.loss))), conn, False
                    )
                else:
                    user.set_user_attr(timerinfo.id, "coins",
                        c_userinfo.coins + round(timerinfo.coins * timerinfo.multiplier), conn, False
                    )
                bot.loop.create_task(_invest_timer_alert(bot, timerinfo, c_userinfo, emojis))

        cur.execute("DELETE FROM invest_timers WHERE time <= 0")
        conn.commit()

        wait_time = time.time() - start_time

        if wait_time < 0:
            other.log(f"Invest timer is {wait_time * -1} seconds behind schedule", "warning")
        else:
            await asyncio.sleep(1 - wait_time)


async def _invest_timer_alert(bot, timerinfo, c_userinfo, emojis):
    try:
        c_user_obj = await user.load_user_obj(bot, timerinfo.id)
    except discord.NotFound:
        return
    except discord.HTTPException:
        return

    if c_userinfo.settings.notifs["investment"]:
        try:
            if timerinfo.failed:
                await message.send_message(None,
                    f"Your investment failed and you lost {round(timerinfo.loss * 100)}% of your investment",
                    title="Investment notification", channel=c_user_obj
                )
            else:
                await message.send_message(None,
                    f"You earned {round(timerinfo.coins * timerinfo.multiplier)} {emojis.coin} from your investment",
                    title="Investment notification", channel=c_user_obj
                )
        except discord.Forbidden:
            pass


async def activity_loop(bot):
    current_activity = 0

    while True:
        await asyncio.sleep(600)

        if current_activity == 0:
            await bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name=f"{len(bot.guilds)} servers and {len(bot.users)} members"
                )
            )
            current_activity = 1

        elif current_activity == 1:
            await bot.change_presence(
                activity=discord.Game(
                    name="t!help"
                )
            )
            current_activity = 0