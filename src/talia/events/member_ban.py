from main import client
from talia.util.guild import get_guild_base
from talia.util.user import get_uid, remove_user


@client.event
async def on_member_ban(member):
    cur = client.conn.cursor()
    gi = get_guild_base(member.guild.id, cur)

    if gi.ud_mode == 2 or gi.ud_mode == 3:
        uid = get_uid(member.id, member.guild.id, cur)
        if uid is not None:
            remove_user(uid, cur)