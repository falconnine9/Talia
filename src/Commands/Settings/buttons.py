"""
Talia Discord Bot
GNU General Public License v3.0
buttons.py (Commands/Settings)

buttons command
"""
from Utils import user, message
from Storage import help_list

#   Command Information   #
name = "buttons"
dm_capable = True
# ~~~~~~~~~~~~~~~~~~~~~~~ #


async def run(bot, msg, conn):
    split_data = msg.content.split(" ")

    if len(split_data) < 2:
        await message.invalid_use(msg, help_list.buttons, "No value given")
        return

    split_data[1] = split_data[1].lower()
    userinfo = user.load_user(msg.author.id, conn)

    if split_data[1] == "enable":
        if not userinfo.settings.reaction_confirm:
            await message.send_error(msg, "Buttons are already enabled")
            return

        userinfo.settings.reaction_confirm = False
        user.set_user_attr(msg.author.id, "settings", userinfo.settings.cvt_dict(), conn)

        await message.send_message(msg, "Buttons have been enabled", title="Enabled")

    elif split_data[1] == "disable":
        if userinfo.settings.reaction_confirm:
            await message.send_error(msg, "Buttons are already disabled")
            return

        userinfo.settings.reaction_confirm = True
        user.set_user_attr(msg.author.id, "settings", userinfo.settings.cvt_dict(), conn)

        await message.send_message(msg, "Buttons have been disabled", title="Disabled")

    else:
        await message.send_error(msg, f"Unknown value: {split_data[1]}")