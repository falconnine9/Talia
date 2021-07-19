"""
Talia Discord Bot
GNU General Public License v3.0
level.py (Commands/General)

level command
"""
from Utils import user, message

name = "level"
dm_capable = True


async def run(args, bot, msg, conn, guildinfo, userinfo):
    await message.send_message(msg, f"""Level {userinfo.level}
{userinfo.xp:,}/{(userinfo.level * 25):,} XP""", title="Your level")