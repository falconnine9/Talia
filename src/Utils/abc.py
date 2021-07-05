"""
Talia Discord Bot
GNU General Public License v3.0
abc.py (Utils)

Abstract Base Classes
"""


class Config:
    def __init__(self, value_dict):
        self.token = value_dict["token"]
        self.owners = value_dict["owners"]
        self.db = value_dict["db"]
        self.backups = value_dict["backups"]
        self.links = value_dict["links"]
        self.full_logging = value_dict["full_logging"]
        self.cache_size = value_dict["cache_size"]

    def cvt_dict(self):
        return {
            "token": self.token,
            "owners": self.owners,
            "db": self.db,
            "backups": self.backups,
            "links": self.links,
            "full_logging": self.full_logging,
            "cache_size": self.cache_size
        }


class Guild:
    def __init__(self, guild_id):
        self.id = guild_id
        self.prefix = "t!"
        self.disabled_channels = []
        self.shop = []

    def cvt_dict(self):
        return {
            "id": self.id,
            "prefix": self.prefix,
            "disabled_channels": self.disabled_channels,
            "shop": self.shop
        }


class User:
    def __init__(self, user_id):
        self.id = user_id
        self.coins = 0
        self.xp = 0
        self.level = 1
        self.edu_level = 1
        self.job = None
        self.pickaxe = None
        self.pet = None
        self.achievements = []
        self.inventory = []
        self.multiplier = 1.0
        self.company = None
        self.showcase = None
        self.hourly = 0
        self.daily = 0
        self.partner = None
        self.parents = []
        self.children = []
        self.settings = Settings(None, None, None).default()
        self.color = [155, 89, 182]
        self.shop_info = ShopInfo(1000)

    def cvt_dict(self):
        return {
            "id": self.id,
            "coins": self.coins,
            "xp": self.xp,
            "level": self.level,
            "edu_level": self.edu_level,
            "job": self.job,
            "pickaxe": self.pickaxe,
            "achievements": self.achievements,
            "inventory": self.inventory,
            "multiplier_boost": self.multiplier,
            "company": self.company,
            "showcase": self.showcase,
            "hourly": self.hourly,
            "daily": self.daily,
            "partner": self.partner,
            "parents": self.parents,
            "children": self.children,
            "settings": self.settings,
            "color": self.color,
            "shop_info": self.shop_info
        }


class Company:
    def __init__(self, discrim):
        self.discrim = discrim
        self.name = ""
        self.ceo = None
        self.members = {}
        self.invites = []
        self.date_created = ""
        self.multiplier_boost = 1.0

    def cvt_dict(self):
        return {
            "discrim": self.discrim,
            "name": self.name,
            "ceo": self.ceo,
            "members": self.members,
            "invites": self.invites,
            "date_created": self.date_created,
            "multiplier_boost": self.multiplier_boost
        }


class Timer:
    def __init__(self, name, time, user, meta):
        self.name = name
        self.time = time
        self.user = user
        self.meta = meta

    def cvt_dict(self):
        return {
            "name": self.name,
            "time": self.time,
            "user": self.user,
            "meta": self.meta
        }


class EduTimer:
    def __init__(self, user_id, time, level):
        self.id = user_id
        self.time = time
        self.level = level

    def cvt_dict(self):
        return {
            "id": self.id,
            "time": self.time,
            "level": self.level
        }


class InvestTimer:
    def __init__(self, user_id, time, coins, multiplier, failed):
        self.id = user_id
        self.time = time
        self.coins = coins
        self.multiplier = multiplier
        self.failed = failed

    def cvt_dict(self):
        return {
            "id": self.id,
            "time": self.time,
            "coins": self.coins,
            "multiplier": self.multiplier,
            "failed": self.failed
        }


class Item:
    def __init__(self, name, worth, item_type, stats):
        self.name = name
        self.worth = worth
        self.type = item_type
        self.stats = stats

    def cvt_dict(self):
        return {
            "name": self.name,
            "worth": self.worth,
            "type": self.type,
            "stats": self.stats
        }

    def __eq__(self, other):
        return (
            self.name == other.name and self.worth == self.worth and
            self.type == other.type and self.stats == other.stats
        )


class Emojis:
    def __init__(self):
        self.coin = None
        self.confetti = None
        self.ping = None

    def cvt_dict(self):
        return {
            "coin": self.coin,
            "confetti": self.confetti,
            "ping": self.ping
        }


class Job:
    def __init__(self, name, xp, level, salary, cooldown):
        self.name = name
        self.xp = xp
        self.level = level
        self.salary = salary
        self.cooldown = cooldown

    def cvt_dict(self):
        return {
            "name": self.name,
            "xp": self.xp,
            "level": self.level,
            "salary": self.salary,
            "cooldown": self.cooldown
        }


class Pickaxe:
    def __init__(self, name, worth, speed, multiplier):
        self.name = name
        self.worth = worth
        self.speed = speed
        self.multiplier = multiplier

    def cvt_dict(self):
        return {
            "name": self.name,
            "worth": self.worth,
            "speed": self.speed,
            "multiplier": self.multiplier
        }


class Pet:
    def __init__(self, name, worth, pet_type, breed):
        self.name = name
        self.worth = worth
        self.type = pet_type
        self.breed = breed

    def cvt_dict(self):
        return {
            "name": self.name,
            "worth": self.worth,
            "type": self.type,
            "breed": self.breed
        }


class Settings:
    def __init__(self, notifs, timernotifs, reaction_confirm):
        self.notifs = notifs
        self.timernotifs = timernotifs
        self.reaction_confirm = reaction_confirm

    def cvt_dict(self):
        return {
            "notifs": self.notifs,
            "timernotifs": self.timernotifs,
            "reaction_confirm": self.reaction_confirm
        }

    def default(self):
        self.notifs = {
            "paid": True,
            "company_invites": True,
            "divorced": True,
            "disowned": True,
            "school": True,
            "investment": True
        }
        self.timernotifs = {
            "work": False,
            "mine": False,
            "sidejob": False,
            "hourly": False,
            "daily": False
        }
        self.reaction_confirm = False
        return self


class ShopInfo:
    def __init__(self, multiplier_cost):
        self.multiplier_cost = multiplier_cost

    def cvt_dict(self):
        return {
            "multiplier_cost": self.multiplier_cost
        }


class BJCard:
    def __init__(self, value, suit, real_value):
        self.value = value
        self.suit = suit
        self.real_value = real_value

    def cvt_dict(self):
        return {
            "value": self.value,
            "suit": self.suit,
            "real_value": self.real_value
        }