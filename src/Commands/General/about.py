"""
Talia Discord Bot
GNU General Public License v3.0
about.py (Commands/General)

about command
"""
from Utils import message
from Storage import meta

name = "about"
dm_capable = True


async def run(args, bot, msg, conn):
    guilds = len(bot.guilds)
    members = len(bot.users)

    fields = [
        ["Servers", f"```{str(guilds)}```"],
        ["Members", f"```{str(members)}```"],
        ["Version", f"```{meta.version}```", False]
    ]

    await message.send_message(msg, title="Talia", thumbnail=bot.user.avatar_url, fields=fields)