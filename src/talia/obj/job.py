class GuildJob:
    def __init__(self, **kw):
        self.job_id = kw["job_id"]
        self.guild = kw["guild"]
        self.name = kw["name"]
        self.s_min = kw["s_min"]
        self.s_max = kw["s_max"]
        self.c_min = kw["c_min"]
        self.c_max = kw["c_max"]


class UserJob:
    def __init__(self, **kw):
        self.user = kw["user"]
        self.name = kw["name"]
        self.s_min = kw["s_min"]
        self.s_max = kw["s_max"]
        self.c_min = kw["c_min"]
        self.c_max = kw["c_max"]
        self.level = kw["level"]
        self.xp = kw["xp"]