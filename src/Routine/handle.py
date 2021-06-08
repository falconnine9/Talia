import datetime
import discord

import Commands
from Utils import user, abc, other

commands = {
    # General
    "help": Commands.General.help,
    "ping": Commands.General.ping,
    "info": Commands.General.info,
    "stats": Commands.General.stats,
    "inventory": Commands.General.inventory,
    "fuse": Commands.General.fuse,
    "school": Commands.General.school,
    "box": Commands.General.box,
    "leaderboard": Commands.General.leaderboard,
    "company": Commands.General.company,
    "showcase": Commands.General.showcase,

    # Earning
    "job": Commands.Earning.job,
    "work": Commands.Earning.work,
    "invest": Commands.Earning.invest,
    "heist": Commands.Earning.heist,
    "pickaxe": Commands.Earning.pickaxe,
    "mine": Commands.Earning.mine,
    "sidejob": Commands.Earning.sidejob,
    "hourly": Commands.Earning.hourly,
    "daily": Commands.Earning.daily,

    # Gambling
    "coinflip": Commands.Gambling.coinflip,
    "dice": Commands.Gambling.dice,
    "blackjack": Commands.Gambling.blackjack,

    # Settings
    "prefix": Commands.Settings.prefix,
    "channels": Commands.Settings.channels,

    # Administration
    "resetinfo": Commands.Administration.resetinfo,
    "resettimers": Commands.Administration.resettimers,
    "setuserattr": Commands.Administration.setuserattr
}


async def command(bot, msg, conn):
    split_data = msg.content.split(" ")

    if split_data[0].lower() not in commands:
        return

    await commands[split_data[0].lower()].run(bot, msg, conn)

    if other.load_config().full_logging:
        cur = conn.cursor()
        cur.execute("SELECT MAX(id) FROM log")
        max_id = cur.fetchone()

        if max_id[0] is None:
            max_id = (0,)

        cur.execute("INSERT INTO log VALUES (?, ?, ?, ?, ?)", (
            max_id[0] + 1, msg.content.split(" ")[0],
            msg.author.id, msg.guild.id,
            datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        ))
        conn.commit()


async def mentioned_users(bot, msg, conn):
    split_data = msg.content.split(" ")

    for arg in split_data:
        if arg.isdigit():
            try:
                mentioned = await bot.fetch_user(int(arg))
            except discord.NotFound:
                continue
            mentioned_userinfo = user.load_user(mentioned.id, conn)
            if mentioned_userinfo is None:
                new_user = abc.User(mentioned.id)
                user.write_user(new_user, conn, False)

    for mention in msg.mentions:
        mentioned_userinfo = user.load_user(mention.id, conn)
        if mentioned_userinfo is None:
            new_user = abc.User(mention.id)
            user.write_user(new_user, conn, False)