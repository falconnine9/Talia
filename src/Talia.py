"""
Talia Discord Bot
GNU General Public License v3.0
Talia.py

Main file for the discord bot

On startup
1. Initializes the configuration file
2. Creates an ssh tunnel to the server hosting the db
 and makes a connection to the database
3. Initializes the database and makes a new bot object
4. Starts the async event loop
"""
import asyncio
import discord
import mysql.connector
import sshtunnel
import traceback

from Routine import init, handle, loop, post_checks
from Utils import guild, user, message, abc, other

other.log("Preparing")
init.config()

db_info = other.load_config().db
if db_info["host"] == "localhost" or db_info["host"] == "127.0.0.1":
    other.log(f"Opening connection to local database ({db_info['database']})")
    conn = mysql.connector.connect(
        user=db_info["user"], password=db_info["password"],
        host="localhost", port=3306,
        database=db_info["database"]
    )
    other.log("Complete", "success")

else:
    other.log(f"Establishing SSH tunnel connection to {db_info['ssh_username']}@{db_info['host']}")
    with sshtunnel.SSHTunnelForwarder(
        db_info["host"],
        ssh_username=db_info["ssh_username"],
        ssh_password=db_info["ssh_password"],
        remote_bind_address=("127.0.0.1", 22)
    ) as tunnel:
        other.log("Complete", "success")
        other.log(f"Opening connection to remote database ({db_info['database']})")
        conn = mysql.connector.connect(
            user=db_info["user"], password=db_info["password"],
            host=db_info["host"], port=3306,
            database=db_info["database"]
        )
        other.log("Complete")

init.db(conn)
bot = discord.Client(intents=discord.Intents.all())
guild_prefixes = {}


@bot.event
async def on_ready():
    """
    Async event that is called when the program has connected
     to discord and all data has processed

    1. A success log will be made
    2. The main timer, edu timer and invest timer will be
     added to the main event loop
    """
    other.log("Ready", "success")

    bot.loop.create_task(cache_loading_loop())
    bot.loop.create_task(loop.main_timer(conn))
    bot.loop.create_task(loop.edu_timer(bot, conn))
    bot.loop.create_task(loop.invest_timer(bot, conn))


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
    if msg.author.bot:
        return

    if msg.guild is None:
        return

    if bot.user in msg.mentions:
        guildinfo = guild.load_guild(msg.guild.id, conn)

        if guildinfo is not None and msg.channel.id not in guildinfo.disabled_channels:
            emojis = other.load_emojis(bot)
            await message.send_message(msg, f"""I see that you pinged me {emojis.ping}

My prefix is **{guild_prefixes[msg.guild.id]}**
You can use `{guild_prefixes[msg.guild.id]}help` for some help""", title="Hello!")

    try:
        if not msg.content.startswith(guild_prefixes[msg.guild.id]):
            return
    except KeyError:
        guildinfo = guild.load_guild(msg.guild.id, conn)

        if guildinfo is None:
            guild_prefixes[msg.guild.id] = "t!"
        else:
            guild_prefixes[msg.guild.id] = guildinfo.prefix

        if not msg.content.startswith(guild_prefixes[msg.guild.id]):
            return

    guildinfo = guild.load_guild(msg.guild.id, conn)
    if guildinfo is None:
        guildinfo = abc.Guild(msg.guild.id)
        guild.write_guild(guildinfo, conn, False)

    if not msg.channel.permissions_for(msg.guild.me).send_messages:
        return

    if msg.channel.id in guildinfo.disabled_channels:
        return

    userinfo = user.load_user(msg.author.id, conn)
    if userinfo is None:
        userinfo = abc.User(msg.author.id)
        user.write_user(userinfo, conn, False)

    msg.content = msg.content.strip()[len(guild_prefixes[msg.guild.id]):]

    await handle.mentioned_users(bot, msg, conn)
    conn.commit()

    try:
        await handle.command(bot, msg, conn)
    except Exception as errmsg:
        excinfo = traceback.format_exc()
        await message.send_error(msg, f"""\u26a0 An unexpected error occurred \u26a0
Error type: {type(errmsg).__name__}""")
        other.log(f"Error occurred, traceback below\n{excinfo}", "critical")
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
    4. Gets guild numbers and members per guild
    5. Puts the stat information int a file
    """
    cur = conn.cursor()
    while True:
        cur.execute("SELECT id, prefix FROM guilds")
        all_prefixes = cur.fetchall()

        for prefix in all_prefixes:
            guild_prefixes[prefix[0]] = prefix[1]

        guild_num = 0
        member_num = 0
        for guild_ in bot.guilds:
            guild_num += 1
            member_num += len([member for member in guild_.members if not member.bot])

        with open("stat_cache", "w") as f:
            f.write(f"{guild_num},{member_num}")

        await asyncio.sleep(600)


if __name__ == "__main__":
    other.log("Establishing connection to discord")
    try:
        bot.run(other.load_config().token)
    except discord.LoginFailure:
        other.log("Invalid token passed", "critical")