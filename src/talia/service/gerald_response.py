import random

from main import client
from talia.util.guild_ext.dc import get_all_dc
from talia.util.guild_ext.ds import get_all_ds

_responses = {}


async def _await_message():
    def confirm(msg_):
        return (msg_.author.id == 555816892141404163 and
                msg_.content in _responses.keys())
    return await client.wait_for("message", timeout=None, check=confirm)


class ServiceInfo:
    name = "gerald_response"
    desc = "Respond to a gerald activity message"
    can_be_disabled = True


@client.service(ServiceInfo)
async def main():
    while True:
        msg = await _await_message()
        cur = client.conn.cursor()

        ds = get_all_ds(msg.guild.id, cur)
        if "gerald_response" in ds:
            return

        dc = get_all_dc(msg.guild.id, cur)
        if msg.channel.id in dc:
            return

        if type(_responses[msg.content]) == str:
            response = _responses[msg.content]
        else:
            response = random.choice(_responses[msg.content])
        await msg.channel.send(response)