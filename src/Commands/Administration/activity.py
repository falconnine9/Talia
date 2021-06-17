"""
Talia Discord Bot
GNU General Public License v3.0
activity.py (Commands/Administration)

activity command
"""
import discord
import os
from Utils import message, other


async def run(bot, msg, conn):
    await message.send_message(msg, "This command is still in development")

    """
    BROKEN CODE: NEEDS TO BE FIXED
    
    if msg.author.id not in other.load_config().owners:
        await message.send_error(msg, "You have insufficient permissions to use this command")
        return

    split_data = msg.content.split(" ")

    if len(split_data) < 2:
        await message.send_error(msg, "No activity given")
        return

    activity = " ".join(split_data[1:])

    if len(activity) > 128:
        await message.send_error(msg, "Activity is too big")
        return

    activity = _format_activity(activity)

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.custom, name=activity))
    await message.send_message(msg, f"Activity changed to: {activity}", title="Activity changed")
    """


def _format_activity(activity):
    if "{servercount}" in activity:
        if os.path.exists("stat_cache"):
            with open("stat_cache") as stat_f:
                split_stats = stat_f.read().split(",")
                activity.replace("{servercount}", split_stats[0])
        else:
            activity.replace("{servercount}", "0")

    if "{membercount}" in activity:
        if os.path.exists("stat_cache"):
            with open("stat_cache") as stat_f:
                split_stats = stat_f.read().split(",")
                activity.replace("{membercount}", split_stats[1])
        else:
            activity.replace("{membercount}", "0")

    return activity