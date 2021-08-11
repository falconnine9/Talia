import random

from main import client
from talia.util.console import log

_messages = ["Ready", "Ready, hello there", "I'm ready"]


@client.event
async def on_ready():
    log(random.choice(_messages))