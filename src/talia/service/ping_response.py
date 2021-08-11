import random

from main import client
from talia.const import URL
from talia.util.guild import get_prefix
from talia.util.guild_ext.dc import get_all_dc
from talia.util.guild_ext.ds import get_all_ds
from talia.util.message import send_embed

_titles = ["Hi", "Hello", "Hellloooo"]


async def _await_message():
    def confirm(msg_):
        return not msg_.author.bot and client.user in msg_.mentions
    return await client.wait_for("message", timeout=None, check=confirm)


class ServiceInfo:
    name = "ping_response"
    desc = "Respond to a ping with some help"
    can_be_disabled = True


@client.service(ServiceInfo)
async def main():
    while True:
        msg = await _await_message()
        cur = client.conn.cursor()

        ds = get_all_ds(msg.guild.id, cur)
        if "ping_response" in ds:
            return

        dc = get_all_dc(msg.guild.id, cur)
        if msg.channel.id in dc:
            return

        prefix = get_prefix(msg.guild.id, client.conn, confirm=True)
        await send_embed(
            msg,
            desc=(f"My prefix is **{prefix}**\n"
                  f"You can use `{prefix}help` for some help\n"
                  f"Or change your settings on my [dashboard]({URL})"),
            title=random.choice(_titles)
        )