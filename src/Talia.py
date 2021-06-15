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
    other.log("Opening connection to local database")
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
        other.log("Opening connection to remote database")
        conn = mysql.connector.connect(
            user=db_info["user"], password=db_info["password"],
            host=db_info["host"], port=3306,
            database=db_info["database"]
        )
        other.log("Complete")

init.db(conn)
bot = discord.Client(intents=discord.Intents.all())


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

    bot.loop.create_task(loop.main_timer(bot, conn))
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
    if msg.guild is None:
        return

    if msg.author.bot:
        return

    if bot.user in msg.mentions:
        guildinfo = guild.load_guild(msg.guild.id, conn)

        if guildinfo is not None and msg.channel.id not in guildinfo.disabled_channels:
            emojis = other.load_emojis(bot)
            await message.send_message(msg, f"""I see that you pinged me {emojis.ping}

My prefix is **{guildinfo.prefix}**
You can use `{guildinfo.prefix}help` for some help""", title="Hello!")

    if not msg.content.startswith(guild.load_guild_prefix(msg.guild.id, conn)):
        return

    if not msg.channel.permissions_for(msg.guild.me).send_messages:
        return

    guildinfo = guild.load_guild(msg.guild.id, conn)
    if guildinfo is None:
        guildinfo = abc.Guild(msg.guild.id)
        guild.write_guild(guildinfo, conn, False)

    if msg.channel.id in guildinfo.disabled_channels:
        return

    userinfo = user.load_user(msg.author.id, conn)
    if userinfo is None:
        userinfo = abc.User(msg.author.id)
        user.write_user(userinfo, conn, False)

    msg.content = msg.content.strip()[len(guildinfo.prefix):]

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


if __name__ == "__main__":
    other.log("Establishing connection to discord")
    try:
        bot.run(other.load_config().token)
    except discord.LoginFailure:
        other.log("Invalid token passed", "critical")