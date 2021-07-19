"""
Talia Discord Bot
GNU General Public License v3.0
Talia.py

Main file for the discord bot
"""
import time
load_start = time.time()

import asyncio
import discord
import discord_components
import os
import threading
import traceback
from Routine import Console, init, handle, loop, post_checks
from Utils import guild, message, abc, other
from Service import poll

# This sets each environment variable
_environ = [
    "ctl",
    "mtl", "mtl_a",
    "etl", "etl_a",
    "itl", "itl_a",
    "al"
]
for env in _environ:
    os.environ[env] = "1"

# This will open and print the header text
with open("header.txt") as header_f:
    print(header_f.read() + "\n")

other.log("Preparing")
other.log("Initializing configuration file")
init.config()
other.log("Complete", "success")

conn = init.open_main_database(other.load_config().db)
bot = discord.Client(intents=discord.Intents.all(), max_messages=other.load_config().cache_size)
bot.activity = discord.Game(name="t!help")
full_logging = other.load_config().full_logging

other.log("Initializing the database")
init.db(conn)
other.log("Complete", "success")


@bot.event
async def on_ready():
    """
    Async event that is called when the program has connected
     to discord and all data has processed

    1. A success log will be made
    2. Puts each timer into the main loop
    3. Starts the console thread
    """
    other.log(f"Ready ({round(time.time() - load_start, 2)} seconds)", "success")
    discord_components.DiscordComponents(bot)

    bot.loop.create_task(cache_loading_loop())
    bot.loop.create_task(loop.main_timer(bot, conn))
    bot.loop.create_task(loop.edu_timer(bot, conn))
    bot.loop.create_task(loop.invest_timer(bot, conn))
    bot.loop.create_task(loop.activity_loop(bot))

    c_thread = threading.Thread(target=Console.console.run, args=(conn,))
    c_thread.start()


@bot.event
async def on_guild_join(new_guild):
    """
    Async event that is called when the client has been
     added to a new server

    1. An info log will be made
    2. The new guild will be written to the database
    """
    other.log(f"Added to guild {new_guild.name} ({new_guild.id})")
    new_guild = abc.Guild(new_guild.id)
    guild.write_guild(new_guild, conn)


@bot.event
async def on_guild_remove(remove_guild):
    """
    Async event that is called when the client has been
     removed from a server

    1. An info log will be made
    2. The guild will be deleted from the database
    """
    other.log(f"Removed from guild {remove_guild.name} ({remove_guild.id})")
    cur = conn.cursor()
    cur.execute("DELETE FROM guilds WHERE id = %s", (remove_guild.id,))
    conn.commit()


@bot.event
async def on_message(msg):
    """
    Async event that is called when a message has been
     received

    1. Verification that the message can be processed
    2. Check to see if it starts with the guild prefix
    3. Handle some database stuff
    4. Send the message to the command handler
    """
    poll.message_services(bot, msg, conn)

    if msg.author.bot:
        return

    if not handle.prefix(msg, conn):
        return

    if msg.guild is None:
        guild_changed = False
        msg.content = msg.content[2:].strip()
    else:
        guild_changed, guildinfo = handle.verify_guild(msg, conn)
        msg.content = msg.content[len(os.environ[f"TaliaPrefix.{msg.guild.id}"]):].strip()

        if not msg.channel.permissions_for(msg.guild.me).send_messages:
            return

        if msg.channel.id in guildinfo.disabled_channels:
            return

    user_changed = handle.verify_user(msg, conn)
    mentioned_changed = await handle.mentioned_users(bot, msg, conn)

    if guild_changed or user_changed or mentioned_changed:
        conn.commit()

    try:
        await handle.command(bot, msg, conn, full_logging)

    except Exception as errmsg:
        exc_info = traceback.format_exc()
        await message.send_error(msg,
            f"\u26a0 An unexpected error occurred \u26a0\nError type: {type(errmsg).__name__}"
        )
        other.log(f"Error occurred, traceback below\n{exc_info}", "critical")
        return

    await post_checks.level(bot, msg, conn)
    await post_checks.achievements(bot, msg, conn)


async def cache_loading_loop():
    """
    An async loop that is called once every 10 minutes.
     It is used to load stat information and guild
     prefixes into the cache

    1. Creates a cursor object that will always be used
    2. Fetches all prefixes from the database
    3. Places each one into the cache
    """
    cur = conn.cursor()
    while os.environ["ctl"] == "1":
        cur.execute("SELECT id, prefix FROM guilds")
        all_prefixes = cur.fetchall()

        for prefix in all_prefixes:
            os.environ[f"TaliaPrefix.{prefix[0]}"] = prefix[1]

        config = other.load_config()

        global full_logging
        full_logging = config.full_logging

        await asyncio.sleep(3600)


if __name__ == "__main__":
    other.log("Establishing connection to discord")
    try:
        bot.run(other.load_config().token)
    except discord.LoginFailure:
        other.log("Invalid token passed", "critical")