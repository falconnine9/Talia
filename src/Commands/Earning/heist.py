"""
Talia Discord Bot
GNU General Public License v3.0
heist.py (Commands/Earning)

heist command
"""
from Utils import message

name = "heist"
dm_capable = True


async def run(args, bot, msg, conn, guildinfo, userinfo):
    await message.send_error(msg, "This command is still in development")