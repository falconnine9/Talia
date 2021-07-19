"""
Talia Discord Bot
GNU General Public License v3.0
buttons.py (Commands/Settings)

buttons command
"""
from Utils import user, message
from Storage import help_list

name = "buttons"
dm_capable = True


async def run(args, bot, msg, conn):
    if len(args) < 2:
        await message.invalid_use(msg, help_list.buttons, "No value given")
        return

    args[1] = args[1].lower()
    userinfo = user.load_user(msg.author.id, conn)

    if args[1] == "enable":
        if not userinfo.settings.reaction_confirm:
            await message.send_error(msg, "Buttons are already enabled")
            return

        userinfo.settings.reaction_confirm = False
        user.set_user_attr(msg.author.id, "settings", userinfo.settings.cvt_dict(), conn)

        await message.send_message(msg, "Buttons have been enabled", title="Enabled")

    elif args[1] == "disable":
        if userinfo.settings.reaction_confirm:
            await message.send_error(msg, "Buttons are already disabled")
            return

        userinfo.settings.reaction_confirm = True
        user.set_user_attr(msg.author.id, "settings", userinfo.settings.cvt_dict(), conn)

        await message.send_message(msg, "Buttons have been disabled", title="Disabled")

    else:
        await message.send_error(msg, f"Unknown value: {args[1]}")