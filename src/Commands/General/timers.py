"""
Talia Discord Bot
GNU General Public License v3.0
timers.py (Commands/General)

timers command
"""
import discord
from Utils import user, timer, message
from Storage import meta

#   Command Information   #
name = "timers"
dm_capable = True
# ~~~~~~~~~~~~~~~~~~~~~~~ #


async def run(bot, msg, conn):
    split_data = msg.content.split(" ")

    if len(split_data) < 2:
        split_data.append(str(msg.author.id))
    else:
        split_data[1] = split_data[1].replace("<@", "").replace("!", "").replace(">", "")

    try:
        person = await user.load_user_obj(bot, int(split_data[1]))
    except ValueError:
        await message.send_error(msg, "Invalid user")
        return
    except discord.NotFound:
        await message.send_error(msg, "I can't find that person")
        return
    except discord.HTTPException:
        await message.send_error(msg, "An error occurred and the command couldn't be run")
        return

    if person.bot:
        await message.send_error(msg, "I can't get the timers of a bot")
        return

    cur = conn.cursor()

    cur.execute("SELECT name, time FROM timers WHERE user = %s", (person.id,))
    main_timers = cur.fetchall()

    cur.execute("SELECT time FROM edu_timers WHERE id = %s", (person.id,))
    edu_timer = cur.fetchone()

    cur.execute("SELECT time FROM invest_timers WHERE id = %s", (person.id,))
    invest_timer = cur.fetchone()

    all_timers = []
    for timer_ in main_timers:
        all_timers.append(f"{meta.timer_names[timer_[0].split('.')[0]]}: {timer.load_time(timer_[1])}")

    if edu_timer is not None:
        all_timers.append(f"School: {timer.load_time(edu_timer[0])}")

    if invest_timer is not None:
        all_timers.append(f"Investment: {timer.load_time(invest_timer[0])}")

    personinfo = user.load_user(person.id, conn)
    
    listOfTimers = ""
    if not all_timers:
        listOfTimers = "No timers to show!"
    else:
        listOfTimers = "\n".join(all_timers)
    
    await message.send_message(msg, listOfTimers, title=f"{str(person)}'s timers", thumbnail=person.avatar_url,
        color=personinfo.color
    )
