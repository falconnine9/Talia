from main import client
from talia.util.console import log


@client.event
async def on_disconnect():
    log("Lost connection to discord")