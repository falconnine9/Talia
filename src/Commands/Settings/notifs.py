"""
Talia Discord Bot
GNU General Public License v3.0
notifs.py (Commands/Settings)

notifs command
"""
from Utils import user, message
from Storage import help_list


async def run(bot, msg, conn):
    split_data = msg.content.split(" ")

    if len(split_data) < 2:
        await message.invalid_use(msg, help_list.notifs, "No value given")
        return

    userinfo = user.load_user(msg.author.id, conn)
    split_data[1] = split_data[1].lower()

    if split_data[1] == "on":
        if userinfo.settings.notifs:
            await message.send_error(msg, "You already have notifications enabled")
        else:
            userinfo.settings.notifs = True
            user.set_user_attr(msg.author.id, "settings", userinfo.settings.cvt_dict(), conn)
            await message.send_message(msg, "Notifications have been enabled", title="Enabled")

    elif split_data[1] == "off":
        if userinfo.settings.notifs:
            userinfo.settings.notifs = False
            user.set_user_attr(msg.author.id, "settings", userinfo.settings.cvt_dict(), conn)
            await message.send_message(msg, "Notifications have been disabled", title="Disabled")
        else:
            await message.send_error(msg, "You already have notifications disabled")

    else:
        await message.send_error(msg, f"Unknown value: {split_data[1]}")