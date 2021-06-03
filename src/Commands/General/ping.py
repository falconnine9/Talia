from Utils import message


async def run(bot, msg, conn):
    await message.send_message(msg, f"Pong! Latency: {round(bot.latency * 1000)}ms")