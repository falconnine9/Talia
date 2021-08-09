class Command:
    def __init__(self, **kw):
        self.category = kw["category"]
        self.name = kw["name"]
        self.desc = kw["desc"]
        self.args = kw["args"]
        self.uses = kw["uses"]
        self.perms = kw["perms"]
        self.can_be_disabled = kw["can_be_disabled"]
        self.func = kw["func"]