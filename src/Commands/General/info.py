"""
Talia Discord Bot
GNU General Public License v3.0
info.py (Commands/General)

info command
"""
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

    sent_msg = await message.send_message(msg, "Gathering information...")
    personinfo = user.load_user(person.id, conn)

    partner, parents, children = await _load_family_info(bot, personinfo)
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

**--Family--**
Partner: {partner}
Parents: {parents}
Children: {children}

**--Job--**
{jobinfo}

**--Pickaxe--**
{pickaxeinfo}"""
    await message.edit_message(sent_msg, send_str, title=str(person), thumbnail=person.avatar_url)


async def _load_family_info(bot, personinfo):
    if personinfo.partner is None:
        partner = None
    else:
        partner = await bot.fetch_user(personinfo.partner)

    if len(personinfo.parents) == 0:
        parents = None
    else:
        all_parents = []
        for parent in personinfo.parents:
            parent_user = await bot.fetch_user(parent)
            all_parents.append(str(parent_user))
        parents = ", ".join(all_parents)

    if len(personinfo.children) == 0:
        children = None
    else:
        all_children = []
        for child in personinfo.children:
            child_user = await bot.fetch_user(child)
            all_children.append(str(child_user))
        children = ", ".join(all_children)

    return partner, parents, children


def _load_job_info(job):
    if job is None:
        return "No job"
    else:
        return f"""Job: {job.name}
Level: {job.level}
XP: {job.xp}/{job.level * 25} ({round(job.xp / (job.level * 25) * 100)}%)
Job Multiplier: x{round(1 + (job.level / 10) - 0.1, 1)}"""


def _load_pickaxe_info(pickaxe):
    if pickaxe is None:
        return "No Pickaxe"
    else:
        return f"""Pickaxe: {pickaxe.name}
Mining Speed: {pickaxe.speed}
Mining Multiplier: x{pickaxe.multiplier}"""