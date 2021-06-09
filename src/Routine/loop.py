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
from Utils import user, message, other


async def main_timer(bot, conn):
    cur = conn.cursor()
    while True:
        start_time = time.time()

        cur.execute("UPDATE timers SET time = time - 1")
        cur.execute("DELETE FROM timers WHERE time <= 0")
        conn.commit()

        wait_time = time.time() - start_time

        if wait_time < 0:
            other.log(f"Main timer is {wait_time * -1} seconds behind schedule", "warning")
        else:
            await asyncio.sleep(1 - wait_time)


async def edu_timer(bot, conn):
    cur = conn.cursor()
    while True:
        start_time = time.time()

        cur.execute("UPDATE edu_timers SET time = time - 1")
        cur.execute("SELECT * FROM edu_timers WHERE time <= 0")
        completed_users = cur.fetchall()

        for c_user in completed_users:
            user.set_user_attr(c_user[0], "edu_level", c_user[2], conn, False)
            try:
                c_user_obj = await bot.fetch_user(c_user[0])
                await message.send_message(None, "Your education level has been upgraded", channel=c_user_obj)
            except discord.NotFound:
                continue
            except discord.Forbidden:
                continue

        cur.execute("DELETE FROM edu_timers WHERE time <= 0")
        conn.commit()

        wait_time = time.time() - start_time

        if wait_time < 0:
            other.log(f"Edu timer is {wait_time * -1} seconds behind schedule", "warning")
        else:
            await asyncio.sleep(1 - wait_time)


async def invest_timer(bot, conn):
    cur = conn.cursor()
    emojis = other.load_emojis(bot)
    while True:
        start_time = time.time()

        cur.execute("UPDATE invest_timers SET time = time - 1")
        cur.execute("SELECT * FROM invest_timers WHERE time <= 0")
        completed_users = cur.fetchall()

        for c_user in completed_users:
            c_userinfo = user.load_user(c_user[0], conn)
            user.set_user_attr(c_user[0], "coins", c_userinfo.coins + round(c_user[2] * c_user[3]), conn, False)
            try:
                c_user_obj = await bot.fetch_user(c_user[0])
                await message.send_message(None, f"You earned {round(c_user[2] * c_user[3])} {emojis.coin} from your investment", channel=c_user_obj)
            except discord.NotFound:
                continue
            except discord.Forbidden:
                continue

        cur.execute("DELETE FROM invest_timers WHERE time <= 0")
        conn.commit()

        wait_time = time.time() - start_time

        if wait_time < 0:
            other.log(f"Invest timer is {wait_time * -1} seconds behind schedule", "warning")
        else:
            await asyncio.sleep(1 - wait_time)