"""
Talia Discord Bot
GNU General Public License v3.0
handle.py (Routine)

Handles events (Such as commands sent)
"""
import datetime
import discord
import os
import time
import Commands
from Utils import guild, user, message, abc

_commands = {
    # General
    "help": Commands.General.help,
    "about": Commands.General.about,
    "ping": Commands.General.ping,
    "info": Commands.General.info,
    "inventory": Commands.General.inventory,
    "shop": Commands.General.shop,
    "boostshop": Commands.General.boostshop,
    "school": Commands.General.school,
    "box": Commands.General.box,
    "leaderboard": Commands.General.leaderboard,
    "company": Commands.General.company,
    "showcase": Commands.General.showcase,
    "balance": Commands.General.balance,
    "level": Commands.General.level,
    "timers": Commands.General.timers,
    "pay": Commands.General.pay,
    "pet": Commands.General.pet,
    "sell": Commands.General.sell,
    "color": Commands.General.color,

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

    # Actions
    "hug": Commands.Actions.hug,
    "pat": Commands.Actions.pat,
    "kiss": Commands.Actions.kiss,
    "lick": Commands.Actions.lick,
    "slap": Commands.Actions.slap,
    "kill": Commands.Actions.kill,

    # Settings
    "prefix": Commands.Settings.prefix,
    "channels": Commands.Settings.channels,
    "shopitem": Commands.Settings.shopitem,
    "notifs": Commands.Settings.notifs,
    "timernotifs": Commands.Settings.timernotifs,
    "buttons": Commands.Settings.buttons,

    # Administration
    "resetinfo": Commands.Administration.resetinfo,
    "resettimers": Commands.Administration.resettimers,
    "setuserattr": Commands.Administration.setuserattr,
    "update": Commands.Administration.update,
    "proc": Commands.Administration.proc
}

_command_alias = {
    # General
    "p": Commands.General.ping,
    "latency": Commands.General.ping,
    "i": Commands.General.info,
    "information": Commands.General.info,
    "inv": Commands.General.inventory,
    "bs": Commands.General.boostshop,
    "lb": Commands.General.leaderboard,
    "bal": Commands.General.balance,
    "b": Commands.General.balance,
    "lvl": Commands.General.level,
    "l": Commands.General.level,
    "t": Commands.General.timers,

    # Earning
    "w": Commands.Earning.work,
    "m": Commands.Earning.mine,
    "sj": Commands.Earning.sidejob,
    "h": Commands.Earning.hourly,
    "d": Commands.Earning.daily,

    # Gambling
    "cf": Commands.Gambling.coinflip,
    "bj": Commands.Gambling.blackjack,

    # Settings
    "tn": Commands.Settings.timernotifs
}


def prefix(msg, conn):
    if msg.guild is None:
        if not msg.content.startswith("t!"):
            return False

    else:
        try:
            if not msg.content.startswith(os.environ[f"TaliaPrefix.{msg.guild.id}"]):
                return False
        except KeyError:
            guildinfo = guild.load_guild(msg.guild.id, conn)

            if guildinfo is None:
                os.environ[f"TaliaPrefix.{msg.guild.id}"] = "t!"
            else:
                os.environ[f"TaliaPrefix.{msg.guild.id}"] = guildinfo.prefix

            if not msg.content.startswith(os.environ[f"TaliaPrefix.{msg.guild.id}"]):
                return False

    return True


def verify_guild(msg, conn):
    guildinfo = guild.load_guild(msg.guild.id, conn)

    if guildinfo is None:
        guildinfo = abc.Guild(msg.guild.id)
        guild.write_guild(guildinfo, conn, False)
        return True, guildinfo

    return False, guildinfo


def verify_user(msg, conn):
    userinfo = user.load_user(msg.author.id, conn)

    if userinfo is None:
        userinfo = abc.User(msg.author.id)
        user.write_user(userinfo, conn, False)
        return True, userinfo

    return False, userinfo


async def mentioned_users(args, bot, msg, conn):
    """
    Adds all mentioned users in a message to the
     database

    1. Splits the message into arguments by spaces
    2. Checks each argument for a non-mention
     user ID
    3. Checks all the mentions of users
    """
    ret_val = False

    for arg in [arg for arg in args if arg.isdigit()]:
        try:
            mentioned = await user.load_user_obj(bot, int(arg))
        except (discord.NotFound, discord.HTTPException):
            continue

        mentioned_userinfo = user.load_user(mentioned.id, conn)
        if mentioned_userinfo is None:
            new_user = abc.User(mentioned.id)
            user.write_user(new_user, conn, False)
            ret_val = True

    for mention in msg.mentions:
        mentioned_userinfo = user.load_user(mention.id, conn)
        if mentioned_userinfo is None:
            new_user = abc.User(mention.id)
            user.write_user(new_user, conn, False)
            ret_val = True

    return ret_val


async def command(args, bot, msg, conn, guildinfo, userinfo, full_logging):
    """
    Ran by the main Talia.py file when a command
     is given

    1. It will split the message by spaces and checks
     if the first argument is a command
    2. It runs the command
    3. If full logging is enabled, it will log the
     command that was run
    """
    args[0] = args[0].lower()

    if msg.guild is None:
        if args[0] in _commands:
            command_ = _commands[args[0]]

            if not command_.dm_capable:
                await message.send_error(msg, "This command can only be run in servers")
                return

        else:
            if args[0] in _command_alias:
                command_ = _command_alias[args[0]]

                if not command_.dm_capable:
                    await message.send_error(msg, "This command can only be run in servers")
                    return
            else:
                return

    else:
        if args[0] in _commands:
            command_ = _commands[args[0]]
        else:
            if args[0] in _command_alias:
                command_ = _command_alias[args[0]]
            else:
                return

    start_time = time.time()
    await command_.run(args, bot, msg, conn, guildinfo, userinfo)

    if full_logging:
        cur = conn.cursor()
        cur.execute("SELECT MAX(id) FROM log")
        max_id = cur.fetchone()

        if max_id[0] is None:
            max_id = (0,)

        if msg.guild is None:
            cur.execute("INSERT INTO log VALUES (%s, %s, %s, %s, %s, %s)", (
                max_id[0] + 1, args[0],
                msg.author.id, None,
                datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
                round((time.time() - start_time) * 1000)
            ))
        else:
            cur.execute("INSERT INTO log VALUES (%s, %s, %s, %s, %s, %s)", (
                max_id[0] + 1, args[0],
                msg.author.id, msg.guild.id,
                datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
                round((time.time() - start_time) * 1000)
            ))

    user.set_user_attr(msg.author.id, "commands", userinfo.commands + 1, conn, False)
    return True