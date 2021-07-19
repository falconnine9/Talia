"""
Talia Discord Bot
GNU General Public License v3.0
ping.py (Commands/General)

ping command
"""
import time
from Utils import message

name = "ping"
dm_capable = True


async def run(args, bot, msg, conn):
    start_time = time.time()
    conn.ping(reconnect=False, attempts=1, delay=0)
    end_time = time.time()

    await message.send_message(msg, f"""Pong!
**Latency**: {round(bot.latency * 1000)}ms
**DB Latency**: {round((end_time - start_time) * 1000)}ms""")