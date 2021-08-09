from main import client
from talia.util.console import log


@client.event
async def on_resumed():
    log("Resumed connection to discord")