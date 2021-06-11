"""
Talia Discord Bot
GNU General Public License v3.0
handle.py (Routine)

Handles events (Such as commands sent)
"""
import datetime
import discord
import Commands
from Utils import guild, user, abc, other

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
    "bal": Commands.General.bal,
    "timers": Commands.General.timers,

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

    # Family
    "marry": Commands.Family.marry,
    "divorce": Commands.Family.divorce,
    "adopt": Commands.Family.adopt,
    "disown": Commands.Family.disown,
    "runaway": Commands.Family.runaway,

    # Gambling
    "coinflip": Commands.Gambling.coinflip,
    "dice": Commands.Gambling.dice,
    "blackjack": Commands.Gambling.blackjack,

    # Settings
    "prefix": Commands.Settings.prefix,
    "channels": Commands.Settings.channels,
    "alias": Commands.Settings.alias,
    "shopitem": Commands.Settings.shopitem,

    # Administration
    "resetinfo": Commands.Administration.resetinfo,
    "resettimers": Commands.Administration.resettimers,
    "setuserattr": Commands.Administration.setuserattr
}


async def command(bot, msg, conn):
    """
    Ran by the main Talia.py file when a command
     is given

    1. It will split the message by spaces and checks
     if the first argument is a command
    2. It runs the command
    3. If full logging is enabled, it will log the
     command that was run
    """
    split_data = msg.content.split(" ")
    split_data[0] = split_data[0].lower()

    if split_data[0] in commands:
        command_ = split_data[0]
    else:
        guildinfo = guild.load_guild(msg.guild.id, conn)
        if split_data[0] in guildinfo.aliases.keys():
            command_ = guildinfo.aliases[split_data[0]]
        else:
            return

    await commands[command_].run(bot, msg, conn)

    if other.load_config().full_logging:
        cur = conn.cursor()
        cur.execute("SELECT MAX(id) FROM log")
        max_id = cur.fetchone()

        if max_id[0] is None:
            max_id = (0,)

        cur.execute("INSERT INTO log VALUES (?, ?, ?, ?, ?)", (
            max_id[0] + 1, command_,
            msg.author.id, msg.guild.id,
            datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        ))
        conn.commit()


async def mentioned_users(bot, msg, conn):
    """
    Adds all mentioned users in a message to the
     database

    1. Splits the message into arguments by spaces
    2. Checks each argument for a non-mention
     user ID
    3. Checks all the mentions of users
    """
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