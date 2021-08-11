class User:
    def __init__(self, **kw):
        self.id = kw["id"]
        self.guild = kw["guild"]
        self.user = kw["user"]
        self.pocket = kw["pocket"]
        self.bank = kw["bank"]
        self.level = kw["level"]
        self.xp = kw["xp"]
        self.multiplier = kw["multiplier"]
        self.commands = kw["commands"]
        self.job = kw["job"]
        self.pickaxe = kw["pickaxe"]
        self.partner = kw["partner"]
        self.parents = kw["parents"]
        self.children = kw["children"]

    @staticmethod
    def default():
        return User(
            id=None,
            guild=None,
            user=None,
            pocket=0,
            bank=0,
            level=1,
            xp=0,
            multiplier=1.0,
            commands=0,
            job=None,
            pickaxe=None,
            partner=None,
            parents=set(),
            children=set()
        )