from main import client

_responses = {}


@client.service(
    name="gerald_response",
    desc="Respond to gerald activity messages",
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
    if msg.author.id != 555816892141404163:
        return False
    if msg.content not in _responses.keys():
        return False
    return True