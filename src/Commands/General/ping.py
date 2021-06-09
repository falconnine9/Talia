"""
Talia Discord Bot
GNU General Public License v3.0
ping.py (Commands/General)

ping command
"""
from Utils import message


async def run(bot, msg, conn):
    await message.send_message(msg, f"Pong! Latency: {round(bot.latency * 1000)}ms")