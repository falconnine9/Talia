"""
Talia Discord Bot
GNU General Public License v3.0
help_list.py (Storage)

A list of help information for each command
"""
# <--- General ---> #

help_ = {
    "desc": "Get a list of commands or details of a command",
    "usage": "help [category/command]",
    "args": {
        "category/command": "The category or command you want details of (Can be empty to get a list of categories)"
    }
}

ping = {
    "desc": "Get the latency of Talia",
    "usage": "ping",
    "args": {}
}

info = {
    "desc": "Get information about someone",
    "usage": "info [user]",
    "args": {
        "user": "The person you want to get information of (Can be empty to get your own)"
    }
}

stats = {
    "desc": "Get some cool stats about Talia",
    "usage": "stats",
    "args": {}
}

inventory = {
    "desc": "Get a list of items in someones inventory",
    "usage": "inventory [user]",
    "args": {
        "user": "The person you want to get the inventory of (Can be empty to get your own)"
    }
}

shop = {
    "desc": "Buy an item or get a list of server shop items",
    "usage": "shop <operation> [item]",
    "args": {
        "operation": "buy/list",
        "item": "The item ID you want to buy (Only needed if buying)"
    }
}

boostshop = {
    "desc": "Buy a boost or get a list of boosts that you can buy",
    "usage": "boostshop <operation> [boost]",
    "args": {
        "operation": "buy/list",
        "boost": "The boost that you want to buy"
    }
}

school = {
    "desc": "Get a higher education level",
    "usage": "school",
    "args": {}
}

box = {
    "desc": "Buy and open a mystery box",
    "usage": "box <operation> [box id]",
    "args": {
        "operation": "buy/list",
        "box id": "The box ID you want to buy (Only needed if buying)"
    }
}

leaderboard = {
    "desc": "See the leaderboard of a certain subject",
    "usage": "leaderboard <lb>",
    "args": {
        "lb": "The leaderboard that you want to see (coins, level, multiplier)"
    }
}

company = {
    "desc": "Manage the company you're in",
    "usage": "company <operation> [company name/user]",
    "args": {
        "operation": "create/leave/invite/kick/disband/info",
        "company/user": "The company name if creating/getting info, or the user if inviting/kicking"
    }
}

showcase = {
    "desc": "Place an item from your inventory in your showcase box",
    "usage": "showcase <item/remove>",
    "args": {
        "item/remove": "The ID of the item in your inventory or \"remove\" to remove the item"
    }
}

balance = {
    "desc": "Get just the your balance of coins",
    "usage": "balance",
    "args": {}
}

level = {
    "desc": "Get just your level and XP",
    "usage": "level",
    "args": {}
}

timers = {
    "desc": "Get a list of timers and cooldowns of someone",
    "usage": "timers [user]",
    "args": {
        "user": "The user you want to get the timers of (Can be empty to get your own)"
    }
}

pay = {
    "desc": "Pay an amount of coins to someone",
    "usage": "pay <user> <amount>",
    "args": {
        "user": "The person you want to pay",
        "amount": "The amount you want to pay"
    }
}

pet = {
    "desc": "Manage your pet",
    "usage": "pet <operation> [pet name]",
    "args": {
        "operation": "buy/sell/list/name",
        "pet name": "The name of the pet (Only needed if buying or naming)"
    }
}

sell = {
    "desc": "Sell an item from your inventory",
    "usage": "sell <item>",
    "args": {
        "item": "The ID of the item in your inventory"
    }
}

color = {
    "desc": "Change your profile color using RGB",
    "usage": "color <red> <green> <blue>",
    "args": {
        "red": "Red value (0-255)",
        "green": "Green value (0-255)",
        "blue": "Blue value (0-255)"
    }
}


# <--- Earning ---> #

job = {
    "desc": "Join, quit, or get a list of jobs",
    "usage": "job <operation> [job]",
    "args": {
        "operation": "join/quit/list",
        "job": "The job you want to join"
    }
}

work = {
    "desc": "Work at your job for coins and XP",
    "usage": "work",
    "args": {}
}

heist = {
    "desc": "Rob the bank to earn lots of money",
    "usage": "heist <contract>",
    "args": {
        "contract": "The ID of the heist contract in your inventory"
    }
}

invest = {
    "desc": "Invest coins to earn back more than you invested (With some risk of losing coins)",
    "usage": "invest <amount> <time>",
    "args": {
        "amount": "The amount you want to invest",
        "time": "How long you want to invest for (short, long)"
    }
}

pickaxe = {
    "desc": "Buy, sell, or get a list of pickaxes",
    "usage": "pickaxe <operation> [pickaxe]",
    "args": {
        "operation": "buy/sell/list",
        "pickaxe": "The ID of pickaxe you want to buy"
    }
}

mine = {
    "desc": "Mine in the caverns with your pickaxe",
    "usage": "mine",
    "args": {}
}

sidejob = {
    "desc": "Do some work at a random side job",
    "usage": "sidejob",
    "args": {}
}

hourly = {
    "desc": "Collect your hourly",
    "usage": "hourly",
    "args": {}
}

daily = {
    "desc": "Collect your daily",
    "usage": "daily",
    "args": {}
}


# <--- Family ---> #

marry = {
    "desc": "Marry someone",
    "usage": "marry <user>",
    "args": {
        "user": "The person that you want to marry"
    }
}

divorce = {
    "desc": "Divorce your partner",
    "usage": "divorce",
    "args": {}
}

adopt = {
    "desc": "Adopt someone",
    "usage": "adopt <user>",
    "args": {
        "user": "The person that you want to adopt"
    }
}

disown = {
    "desc": "Get rid of one of your children",
    "usage": "disown <user>",
    "args": {
        "user": "The person (has to be your child) that you want to disown"
    }
}

runaway = {
    "desc": "Run away from your parents",
    "usage": "runaway",
    "args": {}
}


# <--- Gambling ---> #

coinflip = {
    "desc": "Flip a coin and bet on what side it will land on",
    "usage": "coinflip [side] [bet]",
    "args": {
        "side": "heads/tails",
        "bet": "The amount of coins you want to bet"
    }
}

dice = {
    "desc": "Roll a dice and bet on what side it will land on",
    "usage": "dice [side] [bet]",
    "args": {
        "side": "A number between 1-6",
        "bet": "The amount of coins you want to bet"
    }
}

blackjack = {
    "desc": "Play a game of blackjack",
    "usage": "blackjack [bet]",
    "args": {
        "bet": "The amount of coins you want to bet"
    }
}


# <--- Actions ---> #

hug = {
    "desc": "Hug someone",
    "usage": "hug <user>",
    "args": {
        "user": "The person that you want to hug"
    }
}

pat = {
    "desc": "Pat someone",
    "usage": "pat <user>",
    "args": {
        "user": "The person that you want to pat"
    }
}

kiss = {
    "desc": "Kiss someone",
    "usage": "kiss <user>",
    "args": {
        "user": "The person that you want to kiss"
    }
}

lick = {
    "desc": "Lick someone",
    "usage": "lick <user>",
    "args": {
        "user": "The person you want to lick"
    }
}

slap = {
    "desc": "Slap someone",
    "usage": "slap <user>",
    "args": {
        "user": "The person you want to slap"
    }
}

kill = {
    "desc": "Kill someone",
    "usage": "kill <user>",
    "args": {
        "user": "The person you want to kill"
    }
}


# <--- Settings ---> #

prefix = {
    "desc": "Change the prefix for Talia for the server",
    "usage": "prefix <new prefix>",
    "args": {
        "new prefix": "The new prefix"
    }
}

channels = {
    "desc": "Enable or disable channels where commands can be run",
    "usage": "channels <operation> <channel>",
    "args": {
        "operation": "enable/disable",
        "channel": "The channel to enable or disable"
    }
}

shopitem = {
    "desc": "Create or remove an item in the server shop",
    "usage": "shopitem <operation> <name/id>",
    "args": {
        "operation": "create/remove",
        "name": "The item name (If creating) or item ID if removing"
    }
}

notifs = {
    "desc": "Manage your DM notifications",
    "usage": "notifs",
    "args": {}
}

timernotifs = {
    "desc": "Manage your timer DM notifications",
    "usage": "timernotifs",
    "args": {}
}

buttons = {
    "desc": "Enable or disable buttons (Will use reactions if disabled)",
    "usage": "buttons <value>",
    "args": {
        "value": "enable/disable"
    }
}