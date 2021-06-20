"""
Talia Discord Bot
GNU General Public License v3.0
job.py (Commands/Earning)

job command
"""
import asyncio
import discord_components
from Utils import user, message, abc, other
from Storage import help_list

jobs = {
    "janitor": {
        "showcase": "Janitor",
        "level": 1,
        "salary": [140, 230],
        "cooldown": [140, 240],
    },
    "trucker": {
        "showcase": "Trucker",
        "level": 1,
        "salary": [200, 320],
        "cooldown": [220, 300]
    },
    "security": {
        "showcase": "Security",
        "level": 2,
        "salary": [240, 600],
        "cooldown": [150, 270]
    },
    "paramedic": {
        "showcase": "Paramedic",
        "level": 2,
        "salary": [260, 570],
        "cooldown": [150, 270]
    },
    "developer": {
        "showcase": "Developer",
        "level": 3,
        "salary": [290, 460],
        "cooldown": [80, 130]
    },
    "engineer": {
        "showcase": "Engineer",
        "level": 3,
        "salary": [250, 650],
        "cooldown": [90, 160]
    },
    "ceo": {
        "showcase": "CEO",
        "level": 4,
        "salary": [500, 1000],
        "cooldown": [100, 210]
    }
}

edu_levels = {
    1: "Elementary",
    2: "Highschool",
    3: "College",
    4: "PhD"
}


async def run(bot, msg, conn):
    split_data = msg.content.split(" ")

    if len(split_data) < 2:
        await message.invalid_use(msg, help_list.job, "No operation given")
        return

    split_data[1] = split_data[1].lower()

    if split_data[1] == "join":
        await _job_join(bot, msg, conn, split_data)

    elif split_data[1] == "quit":
        await _job_quit(bot, msg, conn)

    elif split_data[1] == "list":
        await _job_list(bot, msg)

    else:
        await message.send_error(msg, f"Unknown operation: {split_data[1]}")


async def _job_join(bot, msg, conn, split_data):
    if len(split_data) < 3:
        await message.invalid_use(msg, help_list.job, "No job given")
        return

    userinfo = user.load_user(msg.author.id, conn)

    if userinfo.job is not None:
        await message.send_error(msg, "You already have a job")
        return

    split_data[2] = split_data[2].lower()

    if split_data[2] not in jobs:
        await message.send_error(msg, "There's no job with that name")
        return

    if jobs[split_data[2]]["level"] > userinfo.edu_level:
        await message.send_error(msg, """You don't have enough education level to get this job
(Get a higher education level with the `school` command)""")
        return

    user.set_user_attr(msg.author.id, "job", abc.Job(
        jobs[split_data[2]]["showcase"], 0, 1,
        jobs[split_data[2]]["salary"],
        jobs[split_data[2]]["cooldown"]
    ).cvt_dict(), conn)
    await message.send_message(msg, f"You joined the {jobs[split_data[2]]['showcase']} job", title="Joined Job")


async def _job_quit(bot, msg, conn):
    userinfo = user.load_user(msg.author.id, conn)

    if userinfo.job is None:
        await message.send_error(msg, "You don't have a job")
        return

    sent_msg = await message.send_message(msg, "Are you sure you want to quit your job?", title="Quitting..",
        components=[[
            discord_components.Button(label="Confirm", style=discord_components.ButtonStyle.green),
            discord_components.Button(label="Cancel", style=discord_components.ButtonStyle.red)
        ]]
    )

    def button_check(interaction):
        if interaction.author != msg.author:
            return False

        if interaction.message != sent_msg:
            return False

        return True

    try:
        interaction = await bot.wait_for("button_click", timeout=120, check=button_check)
    except asyncio.TimeoutError:
        await message.timeout_response(sent_msg)
        return

    if interaction.component.label == "Cancel":
        await message.response_edit(sent_msg, interaction, sent_msg.embeds[0].description, title="Cancelled")
        return

    userinfo = user.load_user(msg.author.id, conn)

    if userinfo.job is None:
        await message.response_send(sent_msg, interaction, "You don't have a job right now")
        return

    user.set_user_attr(msg.author.id, "job", abc.Job(
        None, 0, 1, [], []
    ).cvt_dict(), conn)
    await message.response_edit(sent_msg, interaction, "You quit your job", title="Quit Job")


async def _job_list(bot, msg):
    fields = []
    emojis = other.load_emojis(bot)

    for job in jobs.keys():
        fields.append([jobs[job]['showcase'], f"""Education Level: {edu_levels[jobs[job]['level']]}
Salary: {jobs[job]['salary'][0]}-{jobs[job]['salary'][1]} {emojis.coin}
Cooldown: {jobs[job]['cooldown'][0]}-{jobs[job]['cooldown'][1]} mins"""])

    await message.send_message(msg, title="Jobs", fields=fields)