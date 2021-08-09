class Service:
    def __init__(self, **kw):
        self.name = kw["name"]
        self.desc = kw["desc"]
        self.can_be_disabled = kw["can_be_disabled"]
        self.func = kw["func"]