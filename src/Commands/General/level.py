"""
Talia Discord Bot
GNU General Public License v3.0
level.py (Commands/General)

level command
"""
from Utils import user, message, other

#   Command Information   #
name = "level"
dm_capable = True
# ~~~~~~~~~~~~~~~~~~~~~~~ #

async def run(bot, msg, conn):
    userinfo = user.load_user(msg.author.id, conn)
    send_str = f"""Level: {userinfo.level} 
    XP: {userinfo.xp}/{userinfo.level * (userinfo.fusion_level * 25)} ({round(userinfo.xp / (userinfo.level * (userinfo.fusion_level * 25)) * 100)}%)
    Multiplier: x{other.load_multi(userinfo, conn)} """

    await message.send_message(msg, send_str, title="Your level")
   