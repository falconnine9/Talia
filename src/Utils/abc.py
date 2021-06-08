class Config:
    def __init__(self, value_dict):
        self.token = value_dict["token"]
        self.owners = value_dict["owners"]
        self.db_path = value_dict["db_path"]
        self.backups = value_dict["backups"]
        self.links = value_dict["links"]
        self.full_logging = value_dict["full_logging"]

    def cvt_dict(self):
        return {
            "token": self.token,
            "owners": self.owners,
            "db_path": self.db_path,
            "backups": self.backups,
            "links": self.links,
            "full_logging": self.full_logging
        }


class Guild:
    def __init__(self, guild_id):
        self.id = guild_id
        self.prefix = "t!"
        self.disabled_channels = []

    def cvt_dict(self):
        return {
            "id": self.id,
            "prefix": self.prefix
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
        self.achievements = []
        self.inventory = []
        self.fusion_level = 1
        self.multiplier = 1.0
        self.company = None
        self.showcase = None
        self.hourly = 0
        self.daily = 0
        self.partner = None
        self.parents = []
        self.children = []

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
            "fusion_level": self.fusion_level,
            "multiplier_boost": self.multiplier,
            "company": self.company,
            "showcase": self.showcase,
            "hourly": self.hourly,
            "daily": self.daily,
            "partner": self.partner,
            "parents": self.parents,
            "children": self.children
        }


class Company:
    def __init__(self, discrim):
        self.discrim = discrim
        self.name = ""
        self.ceo = None
        self.members = {}
        self.invites = []
        self.date_created = ""
        self.multiplier_boost = 0.0

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
    def __init__(self, user_id, time, coins, multiplier):
        self.id = user_id
        self.time = time
        self.coins = coins
        self.multiplier = multiplier

    def cvt_dict(self):
        return {
            "id": self.id,
            "time": self.time,
            "coins": self.coins,
            "multiplier": self.multiplier
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


class Emojis:
    def __init__(self):
        self.coin = None
        self.confetti = None


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
    def __init__(self, name, worth, xp, level, speed, multiplier):
        self.name = name
        self.worth = worth
        self.xp = xp
        self.level = level
        self.speed = speed
        self.multiplier = multiplier

    def cvt_dict(self):
        return {
            "name": self.name,
            "worth": self.worth,
            "xp": self.xp,
            "level": self.level,
            "speed": self.speed,
            "multiplier": self.multiplier
        }


class BJCard:
    def __init__(self, value, suit, real_value):
        self.value = value
        self.suit = suit
        self.real_value = real_value