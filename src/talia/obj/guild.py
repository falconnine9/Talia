class Guild:
    def __init__(self, **kw):
        self.id = kw["id"]
        self.prefix = kw["prefix"]
        self.ud_mode = kw["ud_mode"]
        self.dc = kw["dc"]
        self.dco = kw["dco"]
        self.dcs = kw["dcs"]
        self.jobs = kw["jobs"]
        self.pickaxes = kw["pickaxes"]