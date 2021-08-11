class GuildPickaxe:
    def __init__(self, **kw):
        self.pickaxe_id = kw["pickaxe_id"]
        self.guild = kw["guild"]
        self.name = kw["name"]
        self.cost = kw["cost"]
        self.speed = kw["speed"]
        self.multi = kw["multi"]


class UserPickaxe:
    def __init__(self, **kw):
        self.user = kw["user"]
        self.name = kw["name"]
        self.worth = kw["worth"]
        self.speed = kw["speed"]
        self.multi = kw["multi"]