"""
Talia Discord Bot
GNU General Public License v3.0
leaderboard.py (Commands/General)

leaderboard command
"""
from Utils import message, other
from Storage import help_list

#   Command Information   #
name = "leaderboard"
dm_capable = True
# ~~~~~~~~~~~~~~~~~~~~~~~ #


async def run(bot, msg, conn):
    split_data = msg.content.split(" ")

    if len(split_data) < 2:
        await message.invalid_use(msg, help_list.leaderboard, "No lb given")
        return

    split_data[1] = split_data[1].lower()

    if split_data[1] == "coins":
        await lb_coins(bot, msg, conn)

    elif split_data[1] == "level":
        await lb_level(bot, msg, conn)

    elif split_data[1] == "multiplier":
        await lb_multiplier(bot, msg, conn)

    else:
        await message.send_error(msg, f"Unknown leaderboard\n`coins`, `level`, `multiplier`")


async def lb_coins(bot, msg, conn):
    cur = conn.cursor()
    cur.execute("SELECT id, coins FROM users ORDER BY coins DESC LIMIT 10")
    top_users = cur.fetchall()

    if len(top_users) == 0:
        await message.send_message(msg, "Nothing in here :(", title="Coins Leaderboard")
        return

    user_list = []
    emojis = other.load_emojis(bot)

    for i, user in enumerate(top_users):
        user_obj = bot.get_user(user[0])

        if user_obj is None:
            user_list.append(f"{i + 1}: Unknown#0000 | {user[1]:,} {emojis.coin}")
        else:
            user_list.append(f"{i + 1}. {str(user_obj)} | {user[1]:,} {emojis.coin}")

    await message.send_message(msg, "\n".join(user_list), title="Coins Leaderboard")


async def lb_level(bot, msg, conn):
    cur = conn.cursor()
    cur.execute("SELECT id, level FROM users ORDER BY level DESC LIMIT 10")
    top_users = cur.fetchall()

    if len(top_users) == 0:
        await message.send_message(msg, "Nothing in here :(", title="Level Leaderboard")
        return

    user_list = []

    for i, user in enumerate(top_users):
        user_obj = bot.get_user(user[0])

        if user_obj is None:
            user_list.append(f"{i + 1}: Unknown#0000 | Level {user[1]}")
        else:
            user_list.append(f"{i + 1}. {str(user_obj)} | Level {user[1]}")

    await message.send_message(msg, "\n".join(user_list), title="Level Leaderboard")


async def lb_multiplier(bot, msg, conn):
    cur = conn.cursor()
    cur.execute("SELECT id, multiplier FROM users ORDER BY multiplier DESC LIMIT 10")
    top_users = cur.fetchall()

    if len(top_users) == 0:
        await message.send_message(msg, "Nothing in here :(", title="Multiplier Leaderboard")
        return

    user_list = []

    for i, user in enumerate(top_users):
        user_obj = bot.get_user(user[0])

        if user_obj is None:
            user_list.append(f"{i + 1}: Unknown#0000 | x{user[1]}")
        else:
            user_list.append(f"{i + 1}. {str(user_obj)} | x{user[1]}")

    await message.send_message(msg, "\n".join(user_list), title="Multiplier Leaderboard")