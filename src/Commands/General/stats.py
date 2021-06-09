"""
Talia Discord Bot
GNU General Public License v3.0
stats.py (Commands/General)

stats command
"""
from Utils import message, other
from Storage import meta


async def run(bot, msg, conn):
    cur = conn.cursor()
    cur.execute("SELECT SUM(coins) FROM users")
    sum_coins = cur.fetchone()

    cur.execute("SELECT id FROM edu_timers")
    all_education = cur.fetchall()

    cur.execute("SELECT id FROM invest_timers")
    all_investments = cur.fetchall()

    emojis = other.load_emojis(bot)

    await message.send_message(msg, f"""A total of {sum_coins[0]} {emojis.coin} between everyone
{len(all_education)} people in school
{len(all_investments)} investments running""", title="Talia", thumbnail=bot.user.avatar_url,
        footer=f"Talia version {meta.version}", footer_icon=bot.user.avatar_url
    )