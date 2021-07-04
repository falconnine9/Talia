"""
Talia Discord Bot
GNU General Public License v3.0
handle.py (Routine)

Handles events (Such as commands sent)
"""
import datetime
import discord
import time
import Commands
from Utils import guild, user, message, abc, other

commands = {
    # General
    "help": Commands.General.help,
    "ping": Commands.General.ping,
    "info": Commands.General.info,
    "stats": Commands.General.stats,
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
    "update": Commands.Administration.update
}

command_alias = {
    # General
    "p": Commands.General.ping,
    "latency": Commands.General.ping,
    "i": Commands.General.info,
    "information": Commands.General.info,
    "inv": Commands.General.inventory,
    "bs": Commands.General.boostshop,
    "lb": Commands.General.leaderboard,
    "bal": Commands.General.balance,
    "lvl": Commands.General.level,
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

    if msg.guild is None:
        if split_data[0] in commands:
            command_ = commands[split_data[0]]

            if not command_.dm_capable:
                await message.send_error(msg, "This command can only be run in servers")
                return

        else:
            if split_data[0] in command_alias:
                command_ = command_alias[split_data[0]]

                if not command_.dm_capable:
                    await message.send_error(msg, "This command can only be run in servers")
                    return
            else:
                return

    else:
        if split_data[0] in commands:
            command_ = commands[split_data[0]]
        else:
            if split_data[0] in command_alias:
                command_ = command_alias[split_data[0]]
            else:
                return

    start_time = time.time()
    await command_.run(bot, msg, conn)

    if other.load_config().full_logging:
        cur = conn.cursor()
        cur.execute("SELECT MAX(id) FROM log")
        max_id = cur.fetchone()

        if max_id[0] is None:
            max_id = (0,)

        if msg.guild is None:
            cur.execute("INSERT INTO log VALUES (%s, %s, %s, %s, %s, %s)", (
                max_id[0] + 1, split_data[0],
                msg.author.id, None,
                datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
                round((time.time() - start_time) * 1000)
            ))
        else:
            cur.execute("INSERT INTO log VALUES (%s, %s, %s, %s, %s, %s)", (
                max_id[0] + 1, split_data[0],
                msg.author.id, msg.guild.id,
                datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
                round((time.time() - start_time) * 1000)
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

    for arg in [arg for arg in split_data if arg.isdigit()]:
        try:
            mentioned = await user.load_user_obj(bot, int(arg))
        except discord.NotFound:
            continue
        except discord.HTTPException:
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


async def ping(bot, msg, conn):
    emojis = other.load_emojis(bot)

    if msg.guild is None:
        await message.send_message(msg, await message.send_message(msg, f"""I see that you pinged me {emojis.ping}

My prefix is **t!**
You can use `t!help` for some help""", title="Hello!"))

    else:
        guildinfo = guild.load_guild(msg.guild.id, conn)

        if guildinfo is None:
            return

        if msg.channel.id in guildinfo.disabled_channels:
            return

        await message.send_message(msg, await message.send_message(msg, f"""I see that you pinged me {emojis.ping}

My prefix is **{guildinfo.prefix}**
You can use `{guildinfo.prefix}help` for some help""", title="Hello!"))


def prefix(msg, conn, guild_prefixes):
    if msg.guild is None:
        if not msg.content.startswith("t!"):
            return False

    else:
        try:
            if not msg.content.startswith(guild_prefixes[msg.guild.id]):
                return False
        except KeyError:
            guildinfo = guild.load_guild(msg.guild.id, conn)

            if guildinfo is None:
                guild_prefixes[msg.guild.id] = "t!"
            else:
                guild_prefixes[msg.guild.id] = guildinfo.prefix

            if not msg.content.startswith(guild_prefixes[msg.guild.id]):
                return False

    return True