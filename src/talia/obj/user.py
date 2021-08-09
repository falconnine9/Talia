class User:
    def __init__(self, **kw):
        self.id = kw["id"]
        self.guild = kw["guild"]
        self.user = kw["user"]
        self.coins = kw["coins"]
        self.level = kw["level"]
        self.xp = kw["xp"]
        self.commands = kw["commands"]
        self.job = kw["job"]
        self.pickaxe = kw["pickaxe"]
        self.partner = kw["partner"]
        self.parents = kw["parents"]
        self.children = kw["children"]