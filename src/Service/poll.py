"""
Talia Discord Bot
GNU General Public License v3.0
poll.py (Service)

Handling services when they should be called
"""
from Service import ping_service


def message_services(bot, msg, conn):
    """
    Runs all the message services

    1. Checks to see if the message sent fits the
     criteria for the service to be ran
    2. Puts the service into the bot async loop
    """
    if bot.user in msg.mentions:
        bot.loop.create_task(ping_service.run(bot, msg, conn))