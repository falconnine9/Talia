from main import client
from talia.util.console import log


@client.event
async def on_message(msg):
    log(msg.content)