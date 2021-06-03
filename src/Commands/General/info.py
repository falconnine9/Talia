import discord

from Utils import user, company, message, other

edu_levels = {
    1: "Elementary",
    2: "Highschool",
    3: "College",
    4: "PhD"
}

fusion_levels = {
    1: "Human",
    2: "Tiger",
    3: "Minotaur",
    4: "Gryphon",
    5: "Elephant",
    6: "Reaper",
    7: "Dragon",
    8: "Hydra"
}


async def run(bot, msg, conn):
    split_data = msg.content.split(" ")

    if len(split_data) < 2:
        split_data.append(str(msg.author.id))
    else:
        split_data[1] = split_data[1].replace("<@", "").replace("!", "").replace(">", "")

    try:
        person = await bot.fetch_user(int(split_data[1]))
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
        await message.send_error(msg, "I can't get the information of a bot")
        return

    personinfo = user.load_user(person.id, conn)

    jobinfo = _load_job_info(personinfo.job)
    pickaxeinfo = _load_pickaxe_info(personinfo.pickaxe)

    if personinfo.company is not None:
        companyinfo = company.load_company(personinfo.company, conn)
        company_name = companyinfo.name
    else:
        company_name = "None"

    emojis = other.load_emojis(bot)
    send_str = f"**Level {personinfo.level} {fusion_levels[personinfo.fusion_level]}**"

    if personinfo.showcase is not None:
        send_str += f"\n**| {personinfo.showcase.name} |**"

    send_str += f"""\n\n**--General Information--**
Coins: {personinfo.coins} {emojis.coin}
XP: {personinfo.xp}/{personinfo.level * (personinfo.fusion_level * 25)} ({round(personinfo.xp / (personinfo.level * (personinfo.fusion_level * 25)) * 100)}%)
Multiplier: x{other.load_multi(personinfo, conn)}
Education Level: {edu_levels[personinfo.edu_level]}
Company: {company_name}

**--Job--**
{jobinfo}

**--Pickaxe--**
{pickaxeinfo}"""
    await message.send_message(msg, send_str, title=str(person), thumbnail=person.avatar_url)


def _load_job_info(job):
    if job is None:
        return "No job"
    else:
        return f"""Job: {job.name}
Level: {job.level}
XP: {job.xp}"""


def _load_pickaxe_info(pickaxeinfo):
    if pickaxeinfo is None:
        return "No Pickaxe"
    else:
        return f"""Pickaxe: {pickaxeinfo.name}
Mining Speed: {pickaxeinfo.speed}
Mining Multiplier: x{pickaxeinfo.multiplier}
Level: {pickaxeinfo.level}
XP: {pickaxeinfo.xp}"""