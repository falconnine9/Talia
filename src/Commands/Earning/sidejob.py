"""
Talia Discord Bot
GNU General Public License v3.0
sidejob.py (Commands/Earning)

sidejob command
"""
import random
from Utils import user, timer, message, abc, other

name = "sidejob"
dm_capable = True

_job_messages = [
    "You do some box moving at your local warehouse",
    "You give some rich guy a lap dance",
    "You break open your child's piggy bank",
    "You revise a story written by a local author",
    "You coach the high school football team",
    "You make some music with bottles",
    "You teach night school",
    "You join a delivery service for the day",
    "You help quality assurance test a new game",
    "You draw some interesting art for a commission"
]


async def run(args, bot, msg, conn):
    sidejob_timer = timer.load_timer(f"sidejob.{msg.author.id}", conn)

    if sidejob_timer is not None:
        await message.send_error(msg, f"Wait {timer.load_time(sidejob_timer.time)} before working at a side job again")
        return

    userinfo = user.load_user(msg.author.id, conn)

    earned_coins = round(random.randint(1, 300) * other.load_multi(userinfo, conn))
    earned_xp = round(random.randint(1, 20) * other.load_multi(userinfo, conn))

    user.set_user_attr(msg.author.id, "coins", userinfo.coins + earned_coins, conn, False)
    user.set_user_attr(msg.author.id, "xp", userinfo.xp + earned_xp, conn, False)

    sidejob_timer = abc.Timer(f"sidejob.{msg.author.id}", random.randint(60, 120) * 60, msg.author.id, None)
    timer.new_timer(sidejob_timer, conn)

    emojis = other.load_emojis(bot)

    await message.send_message(msg, f"""{random.choice(_job_messages)}
+{earned_coins:,} {emojis.coin}
+{earned_xp:,} XP""", title="Side job")