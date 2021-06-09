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
    new_emojis = abc.Emojis()

    new_emojis.coin = bot.get_emoji(840419193143689236)
    new_emojis.confetti = bot.get_emoji(840419520468221972)

    return new_emojis


def load_multi(userinfo, conn):
    if userinfo.company is not None:
        company_boost = company.load_company(userinfo.company, conn).multiplier_boost
    else:
        company_boost = 1.0

    return userinfo.multiplier * company_boost