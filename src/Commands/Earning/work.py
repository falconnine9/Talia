"""
Talia Discord Bot
GNU General Public License v3.0
work.py (Commands/Earning)

work command
"""
import random
from Utils import user, timer, message, abc, other

#   Command Information   #
name = "work"
dm_capable = True
# ~~~~~~~~~~~~~~~~~~~~~~~ #


async def run(bot, msg, conn):
    userinfo = user.load_user(msg.author.id, conn)

    if userinfo.job is None:
        await message.send_error(msg,
            "You need a job to work\n(You can join one with the `job` command)")
        return

    job_timer = timer.load_timer(f"work.{msg.author.id}", conn)

    if job_timer is not None:
        await message.send_error(msg,
            f"Wait {timer.load_time(job_timer.time)} before working again")
        return

    coins = round(random.randint(userinfo.job.salary[0], userinfo.job.salary[1]) * other.load_multi(userinfo, conn) * (1 + (userinfo.job.level / 10) - 0.1))
    xp = round(random.randint(1, 25) * other.load_multi(userinfo, conn) * (1 + (userinfo.job.level / 10) - 0.1))
    cooldown_timer = abc.Timer(
        f"work.{msg.author.id}",
        random.randint(userinfo.job.cooldown[0], userinfo.job.cooldown[1]) * 60,
        msg.author.id, None
    )
    userinfo.job.xp += random.randint(1, 25)

    user.set_user_attr(msg.author.id, "coins", userinfo.coins + coins, conn, False)
    user.set_user_attr(msg.author.id, "xp", userinfo.xp + xp, conn, False)
    user.set_user_attr(msg.author.id, "job", userinfo.job.cvt_dict(), conn, False)
    timer.new_timer(cooldown_timer, conn)

    emojis = other.load_emojis(bot)
    await message.send_message(msg,
        f"You worked as a {userinfo.job.name}\n+{coins} {emojis.coin}\n+{xp} XP",
        title="Work")
    await _job_xp_check(msg, conn, userinfo, emojis)


async def _job_xp_check(msg, conn, userinfo, emojis):
    if userinfo.job.xp >= userinfo.job.level * 25:
        userinfo.job.level += 1
        userinfo.job.xp = 0
        user.set_user_attr(msg.author.id, "job", userinfo.job.cvt_dict(), conn)
        await message.send_message(msg,
            f"{emojis.confetti} {str(msg.author)} reached job level {userinfo.job.level} {emojis.confetti}",
            title="Job level up"
        )