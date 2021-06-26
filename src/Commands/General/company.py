"""
Talia Discord Bot
GNU General Public License v3.0
company.py (Commands/General)

company command
"""
import asyncio
import datetime
import discord
import discord_components
from Utils import user, company, message, abc, other
from Storage import help_list

#   Command Information   #
name = "company"
dm_capable = True
# ~~~~~~~~~~~~~~~~~~~~~~~ #


async def run(bot, msg, conn):
    split_data = msg.content.split(" ")

    if len(split_data) < 2:
        await message.invalid_use(msg, help_list.company, "No operation given")
        return

    split_data[1] = split_data[1].lower()

    if split_data[1] == "create":
        await _company_create(msg, conn, split_data)

    elif split_data[1] == "leave":
        await _company_leave(msg, conn)

    elif split_data[1] == "invite":
        await _company_invite(bot, msg, conn, split_data)

    elif split_data[1] == "kick":
        await _company_kick(bot, msg, conn, split_data)

    elif split_data[1] == "disband":
        await _company_disband(bot, msg, conn)

    elif split_data[1] == "info":
        await _company_info(bot, msg, conn, split_data)

    else:
        await message.send_error(msg, f"Unknown operation: {split_data[1]}")


async def _company_create(msg, conn, split_data):
    if len(split_data) < 3:
        await message.invalid_use(msg, help_list.company, "No company name given")
        return

    userinfo = user.load_user(msg.author.id, conn)

    if userinfo.company is not None:
        await message.send_error(msg, "You're already in a company")
        return

    company_name = " ".join(split_data[2:])

    if len(company_name) > 64:
        await message.send_error(msg, "The company name can't be longer than 64 characters")
        return

    for char in company_name:
        if ord(char) < 32 or ord(char) > 126:
            await message.send_error(msg, f"Invalid character: {char}")

    existing_company = company.load_company(company_name.lower(), conn)

    if existing_company is not None:
        await message.send_error(msg, "There's already a company with that name")
        return

    new_company = abc.Company(company_name.lower())
    new_company.name = company_name
    new_company.ceo = msg.author.id
    new_company.members[str(msg.author.id)] = datetime.datetime.now().strftime("%Y/%m/%d")
    new_company.date_created = datetime.datetime.now().strftime("%Y/%m/%d")

    company.write_company(new_company, conn, False)
    user.set_user_attr(msg.author.id, "company", new_company.discrim, conn)
    await message.send_message(msg, f"You created a new company: {new_company.name}", title="Company created")


async def _company_leave(msg, conn):
    userinfo = user.load_user(msg.author.id, conn)

    if userinfo.company is None:
        await message.send_error(msg, "You aren't in a company")
        return

    companyinfo = company.load_company(userinfo.company, conn)

    if companyinfo.ceo == msg.author.id:
        await message.send_error(msg,
            "You're the CEO of the company\nIf you want to leave, you have to disband the party"
        )
        return

    del companyinfo.members[str(msg.author.id)]
    company.set_company_attr(userinfo.company, "members", companyinfo.members, conn, False)
    user.set_user_attr(msg.author.id, "company", None, conn)
    await message.send_message(msg, f"You left {companyinfo.name}")


async def _company_invite(bot, msg, conn, split_data):
    if len(split_data) < 3:
        await message.invalid_use(msg, help_list.company, "No user given")
        return

    userinfo = user.load_user(msg.author.id, conn)

    if userinfo.company is None:
        await message.send_error(msg, "You aren't in a company")
        return

    companyinfo = company.load_company(userinfo.company, conn)

    if companyinfo.ceo != msg.author.id:
        await message.send_error(msg, "You aren't the CEO of the company")
        return

    if len(companyinfo.members) >= 50:
        await message.send_error(msg, "You've reached the limit of 50 company members")
        return

    split_data[2] = split_data[2].replace("<@", "").replace("!", "").replace(">", "")

    try:
        person_id = int(split_data[2])
    except ValueError:
        await message.send_error(msg, "Invalid user")
        return

    if person_id == msg.author.id:
        await message.send_error(msg, "You can't invite yourself to a company")
        return
    else:
        try:
            person = await user.load_user_obj(bot, int(split_data[1]))
        except discord.NotFound:
            await message.send_error(msg, "I can't find that person")
            return
        except discord.HTTPException:
            await message.send_error(msg, "An error occurred and the command couldn't be run")
            return

    if person.bot:
        await message.send_error(msg, "I can't invite a bot to the company")
        return

    personinfo = user.load_user(person.id, conn)

    if personinfo.company is not None:
        await message.send_error(msg, f"{str(person)} is already in a company")
        return

    if str(msg.author.id) in companyinfo.invites:
        await message.send_error(msg, f"{str(person)} has already been invited to the company")
        return

    await message.send_message(msg, f"{str(person)} has been invited to join {companyinfo.name}")

    try:
        sent_msg = await message.send_message(None, f"You've been invited to join {companyinfo.name}", title="Invite",
            channel=person, components=[[
                discord_components.Button(label="Accept", style=discord_components.ButtonStyle.green),
                discord_components.Button(label="Decline", style=discord_components.ButtonStyle.red)
            ]]
        )
    except discord.Forbidden:
        await message.send_error(msg, f"{str(person)} can't receive DMs from me")
        return

    companyinfo.invites.append(person.id)
    company.set_company_attr(userinfo.company, "invites", companyinfo.invites, conn)

    def button_check(interaction):
        if interaction.author != person:
            return False

        if interaction.message != sent_msg:
            return False

        return True

    try:
        interaction = await bot.wait_for("button_click", timeout=300, check=button_check)
    except asyncio.TimeoutError:
        userinfo = user.load_user(msg.author.id, conn)

        if userinfo.company is not None:
            companyinfo = company.load_company(userinfo.company, conn)

            if companyinfo is not None:
                companyinfo.invites.remove(person.id)
                company.set_company_attr(companyinfo.discrim, "invites", companyinfo.invites, conn)

                if userinfo.settings.notifs["company_invites"]:
                    try:
                        await message.send_message(None, f"{str(person)} didn't respond to the invite",
                            channel=msg.author
                        )
                    except discord.Forbidden:
                        pass

        await message.timeout_response(sent_msg)
        return

    if interaction.component.label == "Decline":
        userinfo = user.load_user(msg.author.id, conn)

        if userinfo.company is not None:
            companyinfo = company.load_company(userinfo.company, conn)

            if companyinfo is not None:
                companyinfo.invites.remove(person.id)
                company.set_company_attr(companyinfo.discrim, "invites", companyinfo.invites, conn)

                if userinfo.settings.notifs["company_invites"]:
                    try:
                        await message.send_message(None, f"{str(person)} declined the invite", channel=msg.author)
                    except discord.Forbidden:
                        pass

        await message.response_edit(sent_msg, interaction, sent_msg.embeds[0].description, title="Declined")
        return

    userinfo = user.load_user(msg.author.id, conn)

    companyinfo.invites.remove(person.id)
    company.set_company_attr(companyinfo.discrim, "invites", companyinfo.invites, conn)

    if userinfo.company is None:
        await message.response_edit(sent_msg, interaction, sent_msg.embeds[0].description, title="Invite")
        try:
            await message.send_error(None, "There was a problem with joining the company", channel=person)
        except discord.Forbidden:
            pass
        return

    personinfo = user.load_user(person.id, conn)

    if personinfo.company is not None:
        await message.response_edit(sent_msg, interaction, sent_msg.embeds[0].description, title="Invite")
        if userinfo.settings.notifs["company_invites"]:
            try:
                await message.send_error(None, f"{str(person)} joined another company", channel=msg.author)
            except discord.Forbidden:
                pass
        try:
            await message.send_error(None, "You're already in a company", channel=person)
        except discord.Forbidden:
            pass
        return

    companyinfo = company.load_company(userinfo.company, conn)

    if companyinfo is None:
        await message.response_edit(sent_msg, interaction, sent_msg.embeds[0].description, title="Invite")
        try:
            await message.send_error(None, "There was a problem with joining the company", channel=person)
        except discord.Forbidden:
            pass
        return

    if len(companyinfo.members) >= 50:
        await message.response_edit(sent_msg, interaction, sent_msg.embeds[0].description, title="Invite")
        try:
            await message.send_error(None, "The company no longer has enough space for you", channel=person)
        except discord.Forbidden:
            pass
        return

    companyinfo.members[str(person.id)] = datetime.datetime.now().strftime("%Y/%m/%d")
    user.set_user_attr(person.id, "company", companyinfo.discrim, conn, False)
    company.set_company_attr(companyinfo.discrim, "members", companyinfo.members, conn)

    await message.response_edit(sent_msg, interaction, "You joined the company", title="Joined")

    if userinfo.settings.notifs["company_invites"]:
        try:
            await message.send_message(None, f"{str(person)} joined the company", channel=msg.author)
        except discord.Forbidden:
            pass


async def _company_kick(bot, msg, conn, split_data):
    if len(split_data) < 3:
        await message.invalid_use(msg, help_list.company, "No user given")
        return

    userinfo = user.load_user(msg.author.id, conn)

    if userinfo.company is None:
        await message.send_error(msg, "You're not in a company")
        return

    companyinfo = company.load_company(userinfo.company, conn)

    if companyinfo.ceo != msg.author.id:
        await message.send_error(msg, "You're not the CEO")
        return

    try:
        person_id = int(split_data[2])
    except ValueError:
        await message.send_error(msg, "Invalid user")
        return

    if person_id == msg.author.id:
        await message.send_error(msg, "You can't kick yourself")
        return
    else:
        try:
            person = await user.load_user_obj(bot, int(split_data[1]))
        except discord.NotFound:
            await message.send_error(msg, "I can't find that person")
            return
        except discord.HTTPException:
            await message.send_error(msg, "An error occurred and the command couldn't be run")
            return

    if person.bot:
        await message.send_error(msg, f"{str(person)} isn't in the company")
        return

    if str(person.id) not in companyinfo.members.key():
        await message.send_error(msg, f"{str(person)} isn't in the company")
        return

    personinfo = user.load_user(person.id, conn)

    del companyinfo.members[str(person.id)]
    company.set_company_attr(companyinfo.discrim, "members", companyinfo.members, conn, False)
    user.set_user_attr(person.id, "company", None, conn)

    await message.send_message(msg, f"{str(person)} has been kicked from the company")

    if personinfo.settings.notifs:
        try:
            await message.send_message(None, f"You've been kicked from {companyinfo.name}", channel=person)
        except discord.Forbidden:
            pass


async def _company_disband(bot, msg, conn):
    userinfo = user.load_user(msg.author.id, conn)

    if userinfo.company is None:
        await message.send_error(msg, "You're not in a company")
        return

    companyinfo = company.load_company(userinfo.company, conn)

    if companyinfo.ceo != msg.author.id:
        await message.send_error(msg, "You're not the CEO")
        return

    sent_msg = await message.send_message(msg, f"Are you sure you want to disband {companyinfo.name}",
        title="Disbanding..", components=[[
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

    companyinfo = company.load_company(companyinfo.discrim, conn)

    if companyinfo is None:
        await message.response_send(sent_msg, interaction, "The company no longer exists")
        return

    cur = conn.cursor()
    cur.execute("DELETE FROM companies WHERE discrim = %s", (companyinfo.discrim,))
    cur.execute("UPDATE users SET company = NULL WHERE company = %s", (companyinfo.discrim,))
    conn.commit()

    await message.response_edit(sent_msg, interaction, "Company disbanded", title="Disbanded")


async def _company_info(bot, msg, conn, split_data):
    if len(split_data) < 3:
        userinfo = user.load_user(msg.author.id, conn)

        if userinfo.company is None:
            await message.send_error(msg, "You're not in a company")
            return

        split_data.append(userinfo.company)

    companyinfo = company.load_company(split_data[2].lower(), conn)

    if companyinfo is None:
        await message.send_error(msg, "I can't find that company")
        return

    total_coins = 0
    for member in companyinfo.members.keys():
        memberinfo = user.load_user(int(member), conn)
        if memberinfo is not None:
            total_coins += memberinfo.coins

    try:
        ceo = await user.load_user_obj(bot, companyinfo.ceo)
    except discord.NotFound:
        ceo = companyinfo.ceo
    except discord.HTTPException:
        ceo = companyinfo.ceo

    emojis = other.load_emojis(bot)

    await message.send_message(msg, f"""CEO: {str(ceo)}
Total Coins: {total_coins} {emojis.coin}
Members: {len(companyinfo.members)}/50
Company Multiplier: x{companyinfo.multiplier_boost}""", title=companyinfo.name)