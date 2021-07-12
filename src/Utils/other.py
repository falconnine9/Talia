"""
Talia Discord Bot
GNU General Public License v3.0
other.py (Utils)

Random utilities
"""
import datetime
import json
import os
import sys

try:
    import colorama
    colorama.init()
except ImportError:
    colorama = None

from Utils import company, abc


def log(info, level="info"):
    """
    Logs an event to the console and log.txt file

    1. Creates the default prefix/color
    2. Checks t see if the logging level is different
    3. Prints the timestamp, prefix and info the the console
    4. Writes the timestamp, prefix and info to the log.txt file
    """
    prefix = "[  INFO  ]"
    color = ""

    if level == "success":
        prefix = "[SUCCESS ]"
        if colorama is not None:
            color = colorama.Fore.GREEN

    elif level == "warning":
        prefix = "[WARNING ]"
        if colorama is not None:
            color = colorama.Fore.YELLOW

    elif level == "critical":
        prefix = "[CRITICAL]"
        if colorama is not None:
            color = colorama.Fore.RED

    timestamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    if colorama is None:
        print(f"{timestamp} | {prefix} {info}")
    else:
        print(f"{timestamp} | {color}{prefix} {info}{colorama.Style.RESET_ALL}")

    with open("log.txt", "a") as logf:
        logf.write(f"{timestamp} | {prefix} {info}\n")


def load_config():
    """
    Loads information from the configuration file

    1. Checks to see if a different path for config was given
    2. Reads the information out of the file
    3. Returns a new config object with the information
    """
    if "-config" in sys.argv:
        config_location = sys.argv.index("-config")
        
        if config_location == len(sys.argv) - 1:
            raise IndexError("No path given after -config argument")
        
        if not os.path.exists(f"{sys.argv[config_location + 1]}/config.json"):
            raise FileNotFoundError("No configuration file found in location given")
        
        with open(f"{sys.argv[config_location + 1]}/config.json") as cfg:
            return abc.Config(json.load(cfg))
    
    else:
        with open("config.json") as cfg:
            return abc.Config(json.load(cfg))


def load_emojis(bot):
    """
    Loads some emojis from discord

    1. Creates a new emojis object
    2. Sets each emoji
    3. Returns the emoji object
    """
    new_emojis = abc.Emojis()

    new_emojis.coin = bot.get_emoji(840419193143689236)
    new_emojis.confetti = bot.get_emoji(840419520468221972)
    new_emojis.ping = bot.get_emoji(852309653063729202)

    return new_emojis


def load_multi(userinfo, conn):
    """
    Loads the overall multiplier of a user

    1. Adds the company boost
    2. Returns the user multiplier multiplied by the
     company multiplier
    """
    if userinfo.company is not None:
        company_boost = company.load_company(userinfo.company, conn).multiplier
    else:
        company_boost = 1.0

    return userinfo.multiplier * company_boost


async def load_channel_obj(bot, channel_id):
    channel_obj = bot.get_channel(channel_id)

    if channel_obj is None:
        return await bot.fetch_channel(channel_id)
    else:
        return channel_obj