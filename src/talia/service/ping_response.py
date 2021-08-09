from main import client


@client.service(
    name="ping_response",
    desc="Respond to a ping with some help",
    can_be_disabled=True
)
async def service():
    while True:
        msg = await client.wait_for(
            "message",
            timeout=None,
            check=_verification
        )
        print(msg.content)


def _verification(msg):
    if msg.author.bot:
        return False
    if client.user not in msg.mentions:
        return False
    return True