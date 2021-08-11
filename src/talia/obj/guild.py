from talia.const import DEFAULT_PREFIX


class Guild:
    def __init__(self, **kw):
        self.id = kw["id"]
        self.prefix = kw["prefix"]
        self.ud_mode = kw["ud_mode"]
        self.start_coins = kw["start_coins"]
        self.dc = kw["dc"]
        self.dco = kw["dco"]
        self.ds = kw["ds"]
        self.jobs = kw["jobs"]
        self.pickaxes = kw["pickaxes"]

    @staticmethod
    def default():
        return Guild(
            id=None,
            prefix=DEFAULT_PREFIX,
            ud_mode=0,
            start_coins=0,
            dc=set(),
            dco=set(),
            ds=set(),
            jobs=set(),
            pickaxes=set()
        )