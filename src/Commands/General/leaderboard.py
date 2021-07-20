"""
Talia Discord Bot
GNU General Public License v3.0
leaderboard.py (Commands/General)

leaderboard command
"""
import discord
from Utils import user, message, other
from Storage import help_list

name = "leaderboard"
dm_capable = True


async def run(args, bot, msg, conn, guildinfo, userinfo):
    if len(args) < 2:
        await message.invalid_use(msg, help_list.leaderboard, "No lb given")
        return

    args[1] = args[1].lower()

    if args[1] == "coins":
        await _lb_coins(bot, msg, conn)
    elif args[1] == "level":
        await _lb_level(bot, msg, conn)
    elif args[1] == "multiplier":
        await _lb_multiplier(bot, msg, conn)
    elif args[1] == "hourly":
        await _lb_hourly(bot, msg, conn)
    elif args[1] == "daily":
        await _lb_daily(bot, msg, conn)
    elif args[1] == "fortune":
        await _lb_fortune(bot, msg, conn)
    else:
        await message.send_error(msg, f"Unknown lb\ncoins, level, multiplier, hourly, daily, fortune")


async def _lb_coins(bot, msg, conn):
    cur = conn.cursor()
    cur.execute("SELECT id, coins FROM users ORDER BY coins DESC LIMIT 10")
    top_users = cur.fetchall()

    if len(top_users) == 0:
        await message.send_message(msg, "Nothing in here :(", title="Coins Leaderboard")
        return

    user_list = []
    emojis = other.load_emojis(bot)

    for i, user_ in enumerate(top_users):
        try:
            user_obj = await user.load_user_obj(bot, user_[0])
            user_list.append(f"{i + 1}. {str(user_obj)} | {user_[1]:,} {emojis.coin}")
        except (discord.NotFound, discord.HTTPException):
            user_list.append(f"{i + 1}: Unknown#0000 | {user_[1]:,} {emojis.coin}")

    await message.send_message(msg, "\n".join(user_list), title="Coins Leaderboard")


async def _lb_level(bot, msg, conn):
    cur = conn.cursor()
    cur.execute("SELECT id, level FROM users ORDER BY level DESC LIMIT 10")
    top_users = cur.fetchall()

    if len(top_users) == 0:
        await message.send_message(msg, "Nothing in here :(", title="Level Leaderboard")
        return

    user_list = []

    for i, user_ in enumerate(top_users):
        try:
            user_obj = await user.load_user_obj(bot, user_[0])
            user_list.append(f"{i + 1}. {str(user_obj)} | Level {user_[1]}")
        except (discord.NotFound, discord.HTTPException):
            user_list.append(f"{i + 1}: Unknown#0000 | Level {user_[1]}")

    await message.send_message(msg, "\n".join(user_list), title="Level Leaderboard")


async def _lb_multiplier(bot, msg, conn):
    cur = conn.cursor()
    cur.execute("SELECT id, multiplier FROM users ORDER BY multiplier DESC LIMIT 10")
    top_users = cur.fetchall()

    if len(top_users) == 0:
        await message.send_message(msg, "Nothing in here :(", title="Multiplier Leaderboard")
        return

    user_list = []

    for i, user_ in enumerate(top_users):
        try:
            user_obj = await user.load_user_obj(bot, user_[0])
            user_list.append(f"{i + 1}. {str(user_obj)} | x{user_[1]}")
        except (discord.NotFound, discord.HTTPException):
            user_list.append(f"{i + 1}: Unknown#0000 | x{user_[1]}")

    await message.send_message(msg, "\n".join(user_list), title="Multiplier Leaderboard")


async def _lb_hourly(bot, msg, conn):
    cur = conn.cursor()
    cur.execute("SELECT id, hourly FROM users ORDER BY hourly DESC LIMIT 10")
    top_users = cur.fetchall()

    if len(top_users) == 0:
        await message.send_message(msg, "Nothing in here :(", title="Hourly Leaderboard")
        return

    user_list = []

    for i, user_ in enumerate(top_users):
        try:
            user_obj = await user.load_user_obj(bot, user_[0])
            user_list.append(f"{i + 1}. {str(user_obj)} | {user_[1]} hourlies")
        except (discord.NotFound, discord.HTTPException):
            user_list.append(f"{i + 1}: Unknown#0000 | {user_[1]} hourlies")

    await message.send_message(msg, "\n".join(user_list), title="Hourly Leaderboard")


async def _lb_daily(bot, msg, conn):
    cur = conn.cursor()
    cur.execute("SELECT id, daily FROM users ORDER BY daily DESC LIMIT 10")
    top_users = cur.fetchall()

    if len(top_users) == 0:
        await message.send_message(msg, "Nothing in here :(", title="Daily Leaderboard")
        return

    user_list = []

    for i, user_ in enumerate(top_users):
        try:
            user_obj = await user.load_user_obj(bot, user_[0])
            user_list.append(f"{i + 1}. {str(user_obj)} | {user_[1]} dailies")
        except (discord.NotFound, discord.HTTPException):
            user_list.append(f"{i + 1}: Unknown#0000 | {user_[1]} dailies")

    await message.send_message(msg, "\n".join(user_list), title="Daily Leaderboard")


async def _lb_fortune(bot, msg, conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT u.id, u.coins + i.worth + it.coins
        FROM users u, items i, invest_timers it
        WHERE u.id = i.owner AND u.id = it.id
        ORDER BY u.coins + i.worth + it.coins
        LIMIT 10
    """)
    top_users = cur.fetchall()

    if len(top_users) == 0:
        await message.send_message(msg, "Nothing in here :(", title="Fortune Leaderboard",
            footer="Yeah so this lb might be broken"
        )
        return

    user_list = []
    emojis = other.load_emojis(bot)

    for i, user_ in enumerate(top_users):
        try:
            user_obj = await user.load_user_obj(bot, user_[0])
            user_list.append(f"{i + 1}. {str(user_obj)} | {user_[1]:,} {emojis.coin}")
        except (discord.NotFound, discord.HTTPException):
            user_list.append(f"{i + 1}: Unknown#0000 | {user_[1]:,} {emojis.coin}")

    await message.send_message(msg, "\n".join(user_list), title="Fortune Leaderboard",
        footer="Yeah so this lb might be broken"
    )